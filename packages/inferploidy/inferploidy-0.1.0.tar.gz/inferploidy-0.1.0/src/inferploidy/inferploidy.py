import warnings, math, time, copy, random, os
from contextlib import redirect_stdout, redirect_stderr
import logging, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import cluster, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.decomposition import PCA, IncrementalPCA, TruncatedSVD
from scipy import stats
from scipy.sparse import csr_matrix, csc_matrix
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import NearestNeighbors
import sklearn.linear_model as lm
import anndata
from scipy.signal import medfilt

from scoda.clustering import get_neighbors, clustering_alg, merge_clusters_with_seed
from scoda.clustering import get_cluster_lst_and_sizes, get_cluster_adj_mat_from_adj_dist
from scoda.clustering import initially_detect_major_clusters, convert_adj_mat_dist_to_conn
from scoda.clustering import clustering_subsample, get_normalized_agg_adj_mat

CLUSTERING_AGO = 'lv'
SKNETWORK = True
try:
    from sknetwork.clustering import Louvain
except ImportError:
    print('WARNING: sknetwork not installed. GMM will be used for clustering.')
    CLUSTERING_AGO = 'gm'
    SKNETWORK = False

INFERCNVPY = True
try:
    import infercnvpy as cnv
except ImportError:
    print('ERROR: infercnvpy not installed. Tumor cell identification will not be performed.')
    INFERCNVPY = False

#'''
UMAP_INSTALLED = True
try:
    import umap
except ImportError:
    print('WARNING: umap-learn not installed.')
    UMAP_INSTALLED = False
#'''

MIN_ABS_VALUE = 1e-8


def X_normalize(X, total_sum = 1e4): 
    if isinstance(X, csr_matrix):
        Xd = np.array(X.sum(axis=1)*(1/total_sum) + 1e-8).transpose()[0,:]
        rows = X.tocoo().row
        data = copy.deepcopy(X.data)
        data = data/Xd[rows]
            
        X_sparse = csr_matrix( (data, X.indices, X.indptr), shape = X.shape)        
        return X_sparse
    elif isinstance(X, csc_matrix):
        Xd = np.array(X.sum(axis=1)*(1/total_sum) + 1e-8).transpose()[0,:]
        rows = X.tocoo().row
        data = copy.deepcopy(X.data)
        data = data/Xd[rows]
            
        X_sparse = csc_matrix( (data, X.indices, X.indptr), shape = X.shape)        
        return X_sparse
    else:
        Xd = 1/(X.sum(axis=1)*(1/total_sum) + 1e-8)
        return X.mul(Xd, axis = 0)

    
def X_preprocessing( Xs, log_transformed ):
    
    if not log_transformed:
        
        Xx = X_normalize(Xs)
        if isinstance(Xs, csr_matrix) | isinstance(Xs, csc_matrix):
            Xx.data = np.log2(1 + Xx.data)
        else:
            Xx = np.log2(1 + Xx)
    else:
        Xx = copy.deepcopy(Xs)
        
    return Xx


import warnings

def run_infercnv(adata, ref_key, ref_types, gtf_file, cluster_key = 'cnv_leiden', 
             N_pca = 15, n_neighbors = 10, clust_algo = 'lv', clust_resolution = 2, 
             N_cells_max_for_pca = 60000, scoring = True, pca = True, 
             window_size = 100, n_cores = 4, cnv_filter_quantile = 0, 
             verbose = False, cnv_suffix_to_use = None ):
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if cnv_suffix_to_use is None:
            ## Normalize and log-transform
            '''
            sc.pp.normalize_total(adata, target_sum=1e4)
            sc.pp.log1p(adata)
            #'''        
            #'''
            if hasattr(adata, 'X_log1p'):
                adata = anndata.AnnData(X = adata.X_log1p, obs = adata.obs, var = adata.var)
            else:
                start_time = time.time()
                # Xs = adata.to_df()
                Xs = adata.X
                Xx = X_preprocessing( Xs, log_transformed = False )
                if isinstance(Xx, csc_matrix):
                    adata = anndata.AnnData(X = csc_matrix(Xx), obs = adata.obs, var = adata.var)
                else:
                    adata = anndata.AnnData(X = csr_matrix(Xx), obs = adata.obs, var = adata.var)
                # adata.X = csr_matrix(Xx)
                # del Xs
                # sc.pp.highly_variable_genes(adata, n_top_genes = 2000) # , flavor = 'seurat_v3')
    
                etime = round(time.time() - start_time) 
                if verbose: print('   Preprocessing done (%i). ' % etime, flush = True)
            #'''
            
            # 출력을 숨기기 위해 /dev/null로 리디렉션
            log_level = logging.getLogger().getEffectiveLevel()
            logging.basicConfig(level=logging.ERROR)
    
            # 출력을 숨기기 위해 /dev/null로 리디렉션
            null_file = open(os.devnull, 'w')
            save_stdout = sys.stdout
            save_stderr = sys.stderr
            sys.stdout = null_file
            sys.stderr = null_file
    
            # with open(os.devnull, 'w') as fnull:
            #     with redirect_stdout(fnull), redirect_stderr(fnull):
            try:
                cnv.io.genomic_position_from_gtf(gtf_file, adata, gtf_gene_id='gene_name', 
                                             adata_gene_id=None, inplace=True)
                cnv.tl.infercnv(adata, reference_key = ref_key, reference_cat=ref_types, 
                            window_size=window_size, n_jobs = n_cores)
                success = True
            except:
                success = False
                
            #'''
            # 출력을 복원
            sys.stdout = save_stdout
            sys.stderr = save_stderr
            null_file.close()
    
            logging.getLogger().setLevel(log_level)
            # logging.getLogger().setLevel(logging.NOTSET)    
            #'''    
            X_cnv_key = 'X_cnv'
            X_cnv_pca_key = 'X_cnv_pca'
            cnv_score_key = 'cnv_score'
        else:
            X_cnv_key = 'X_cnv%s' % cnv_suffix_to_use
            X_cnv_pca_key = 'X_cnv_pca%s' % cnv_suffix_to_use
            cnv_score_key = 'cnv_score%s' % cnv_suffix_to_use
            success = True
        
        if success:
            start_time = time.time()
            start_time_a = start_time
            if scoring:
                if verbose: print('PCA .. ', end = '')
                # cnv.tl.pca(adata, n_comps = N_pca) 
                if isinstance(adata.obsm[X_cnv_key], csr_matrix) | isinstance(adata.obsm[X_cnv_key], csc_matrix):
                    X_cnv = np.array(adata.obsm[X_cnv_key].todense())
                else:
                    X_cnv = np.array(adata.obsm[X_cnv_key])
                    
                '''
                for i in range(X_cnv.shape[0]):
                    x = X_cnv[i,:]
                    b1 = x > 0
                    if np.sum(b1) > 0:
                        mnvp = np.min(x[b1])
                        x[b1] = x[b1] - mnvp
                        x[b1][x[b1] > 0] = 0
                        
                    b2 = x < 0
                    if np.sum(b2) > 0:
                        mxvn = np.max(x[b2])
                        x[b2] = x[b2] - mxvn
                        x[b2][x[b2] < 0] = 0
                    
                    X_cnv[i,:] = x
                    
                adata.obsm['X_cnv'] = csr_matrix(X_cnv)
                #'''

                xv = np.abs(np.array(X_cnv)).std(axis = 0)   
                qv = cnv_filter_quantile
                odr = xv.argsort()
                X_cnv = X_cnv[:,odr[int(len(odr)*qv):]]    
                X_pca = pca_subsample( X_cnv, N_components_pca = N_pca, 
                                       N_cells_max_for_pca = N_cells_max_for_pca)

                adata.obsm[X_cnv_pca_key] = X_pca
         
                etime = round(time.time() - start_time) 
                if verbose: print('(%i), Finding neighbors .. ' % int(etime), end = '')
                start_time = time.time()
                # cnv.pp.neighbors(adata, key_added = 'cnv_neighbors', n_neighbors=n_neighbors, n_pcs=N_pca)
                adj = kneighbors_graph(X_pca, int(n_neighbors), mode = 'distance', # 'connectivity', 
                                   include_self=True, n_jobs = 4)
                    
                adata.obsp['cnv_neighbor_graph_distance'] = adj
                adj_conn = convert_adj_mat_dist_to_conn(adj, threshold = 0)
                adata.obsp['cnv_neighbor_graph_connectivity'] = adj_conn
                
                etime = round(time.time() - start_time) 
                if verbose: print('(%i), Clustering .. ' % int(etime), end = '')
                start_time = time.time()
                # cnv.tl.leiden(adata, neighbors_key='cnv_neighbors', key_added=cluster_key, resolution = resolution)                
                N_clusters = find_num_clusters( X_cnv.shape[0], clust_resolution )
                clust_labels_all, obj_tmp, adj = clustering_alg(X_pca, clust_algo = clust_algo, 
                                                        N_clusters = N_clusters, 
                                                        resolution = clust_resolution, 
                                                        N_neighbors = n_neighbors, 
                                                        n_cores = 4, adj_dist = adj) # mode='distance', 
                    
                adata.obs[cluster_key] = clust_labels_all
                
                etime = round(time.time() - start_time) 
                if verbose: print('(%i), Scoring .. ' % int(etime), end = '')
                start_time = time.time()
                cnv.tl.cnv_score(adata, groupby = cluster_key, key_added = cnv_score_key)

                etime = round(time.time() - start_time) 
                
            etime_a = round(time.time() - start_time_a) 
            if verbose: print('(%i) done (%i).' % (int(etime), int(etime_a)))

    if not success:
        return None
    else:
        return adata

    
def find_num_clusters( N, Clustering_resolution = 1 ):
    return int(max(((N*(Clustering_resolution**2))**(1/6))*5, 10))

def pca_subsample(Xx, N_components_pca, N_cells_max_for_pca = 100000):
    
    pca = TruncatedSVD(n_components = int(N_components_pca)) # , algorithm = 'arpack')
    
    if Xx.shape[0] <= N_cells_max_for_pca:
        X_pca = pca.fit_transform(Xx)
    else:
        if isinstance(Xx, pd.DataFrame):
            lst_full = list(Xx.index.values)
            lst_sel = random.sample(lst_full, k= N_cells_max_for_pca)
            pca.fit(Xx.loc[lst_sel, :])
        else:
            lst_full = list(np.arange(Xx.shape[0]))
            lst_sel = random.sample(lst_full, k= N_cells_max_for_pca)
            pca.fit(Xx[lst_sel, :])
            
        # X_pca = Xx.dot(pca.components_.transpose()) 
        X_pca = pca.transform(Xx)
        
    return X_pca


def get_ref_clusters(cluster_label, ref_ind, ref_pct_min, 
                     ref_score = None, cs_quantile = 0.5):

    y_clust = cluster_label
    cnv_clust_lst = list(set(cluster_label))
    cnv_clust_lst.sort()

    b_inc = []
    ref_pct = []
    cs_ave = []
    
    b = ref_ind
    for idx in cnv_clust_lst:
        b = y_clust == idx
        bt = b & ref_ind
        cnt = np.sum(bt)

        if ref_score is not None: 
            cs_ave.append(ref_score[b].mean())
            
        ref_pct.append(cnt/np.sum(b))
        if (cnt >= ref_pct_min*np.sum(b)):
            b_inc.append(True)
        else:
            b_inc.append(False)

    df_tmp = pd.DataFrame( {'b_inc': b_inc, 'ref_pct': ref_pct }, 
                           index = cnv_clust_lst )
    
    if (ref_score is not None) & (cs_quantile > 0):
        b_tmp = df_tmp['b_inc'] == True
        qv = df_tmp.loc[b_tmp, 'cs_ave'].quantile(cs_quantile)
        b_tmp = df_tmp['cs_ave'] <= qv
        df_tmp.loc[b_tmp, 'b_inc'] = True
        # display(df_tmp)
        b_inc = list(df_tmp['b_inc'])

    if np.sum(b_inc) > 0:
        cluster_sel = list(np.array(cnv_clust_lst)[b_inc]) 
    else:
        odr = np.array(ref_pct).argsort()
        cluster_sel = [ cnv_clust_lst[odr[-1]] ]
        # print('ERROR: No reference cell types found.')
    
    return cluster_sel, df_tmp
    

def calculate_tumor_score( X_cnv_df, b_ind_sel, b_ind_merged, b_ind_others,
                           uc_margin = 0.2, z_th = 0 ):

    X_cnv = X_cnv_df
    
    # b0 = (ps_cluster_label.astype(int)).isin( cluster_sel_org )
    b1 = b_ind_sel # (ps_cluster_label.astype(int)).isin( cluster_sel )
    b2 = b_ind_merged # (ps_cluster_label.astype(int)).isin( cluster_added )
    b3 = b_ind_others # (ps_cluster_label.astype(int)).isin( cluster_other )

    mu_ref = X_cnv.loc[b1,:].mean()
    sd_ref = X_cnv.loc[b1,:].std()    
    dist_from_ref = np.abs( X_cnv.sub( mu_ref, axis = 1 )).div(sd_ref, axis = 1 )

    b_stop = False
    if b3.sum() < 2:
        
        dist_from_other = dist_from_ref*2   
        
        zscore = np.abs(mu_ref)/(sd_ref)
        bz = zscore >= z_th
        
        # maj_for_other = ( dist_from_ref.loc[:,bz] > dist_from_other.loc[:,bz] ).mean(axis = 1)
        
        maj_for_other = ( dist_from_ref.loc[:,bz] - dist_from_other.loc[:,bz] ).mean(axis = 1)
        
        # wgt = np.abs(mu_ref-mu_other)/(sd_ref + sd_other)
        # maj_for_other = ( dist_from_ref.loc[:,bz] - dist_from_other.loc[:,bz] ).mul(wgt, axis = 1).mean(axis = 1)
        
        ref_maj_mean = maj_for_other[b1].mean()
        ref_maj_sd = maj_for_other[b1].std() + 1e-10
        
        sf = (ref_maj_mean)/(ref_maj_sd)
        th_maj = ref_maj_mean + ref_maj_sd*sf
        uc_maj_lower = th_maj - ref_maj_sd*sf*uc_margin
        uc_maj_upper = th_maj + ref_maj_sd*sf*uc_margin
    
        ref_maj_mean = 0
        other_maj_mean = 0
        
        b_stop = True
        
    else:        
        mu_other = X_cnv.loc[b3,:].mean()
        sd_other = X_cnv.loc[b3,:].std()
    
        zscore = np.abs(mu_ref - mu_other)/(sd_ref + sd_other)
        bz = zscore >= z_th
        
        dist_from_ref = np.abs( X_cnv.sub( mu_ref, axis = 1 )).div(sd_ref, axis = 1 )
        dist_from_other = np.abs( X_cnv.sub( mu_other, axis = 1 )).div(sd_other, axis = 1 )

        maj_for_other = ( dist_from_ref.loc[:,bz] > dist_from_other.loc[:,bz] ).mean(axis = 1)
        
        # wgt = np.abs(mu_ref -mu_other)/(sd_ref + sd_other)
        # maj_for_other = ( dist_from_ref.loc[:,bz] - dist_from_other.loc[:,bz] ).mul(wgt, axis = 1).mean(axis = 1)
        
        ref_maj_mean = maj_for_other[b1].mean()
        ref_maj_sd = maj_for_other[b1].std()
        
        other_maj_mean = maj_for_other[b3].mean()
        other_maj_sd = maj_for_other[b3].std()
        
        sf = (other_maj_mean - ref_maj_mean)/(ref_maj_sd + other_maj_sd)
        th_maj = ref_maj_mean + ref_maj_sd*sf
        uc_maj_lower = th_maj - ref_maj_sd*sf*uc_margin
        uc_maj_upper = th_maj + other_maj_sd*sf*uc_margin

    thresholds = {'th': th_maj, 'lower': uc_maj_lower, 'upper': uc_maj_upper}
    # majority_means = {'normal': ref_maj_mean, 'tumor': other_maj_mean

    return maj_for_other, b_stop, sf, ref_maj_mean, other_maj_mean, thresholds


def calculate_tumor_score_gmm( X_cnv_df, b_ind_sel, b_ind_merged, b_ind_others,
                           uc_margin = 0.2, z_th = 0, gmm_ncomp_n = 2, gmm_ncomp_t = 3 ):

    X_cnv = X_cnv_df
    
    # b0 = (ps_cluster_label.astype(int)).isin( cluster_sel_org )
    b1 = b_ind_sel # (ps_cluster_label.astype(int)).isin( cluster_sel )
    b2 = b_ind_merged # (ps_cluster_label.astype(int)).isin( cluster_added )
    b3 = b_ind_others # (ps_cluster_label.astype(int)).isin( cluster_other )

    '''
    mu_ref = X_cnv.loc[b1,:].mean()
    sd_ref = X_cnv.loc[b1,:].std()    
    dist_from_ref = np.abs( X_cnv.sub( mu_ref, axis = 1 )).div(sd_ref, axis = 1 )
    '''
    gmm_ref = mixture.GaussianMixture(n_components = int(gmm_ncomp_n), covariance_type = 'diag', random_state = 0)
    gmm_ref.fit( X_cnv.loc[b1,:] )
    dist_from_ref = -gmm_ref.score_samples( X_cnv ) ## score_samples: log-likelihood
    dist_from_ref = pd.Series(dist_from_ref, index = X_cnv.index)
    
    b_stop = False
    if b3.sum() < 2:
        
        dist_from_other = dist_from_ref*2   
        
        # zscore = np.abs(mu_ref)/(sd_ref)
        # bz = zscore >= z_th
        
        # maj_for_other = ( dist_from_ref.loc[:,bz] > dist_from_other.loc[:,bz] ).mean(axis = 1)
        
        maj_for_other = ( dist_from_ref - dist_from_other ) # .mean(axis = 1)
        
        # wgt = np.abs(mu_ref-mu_other)/(sd_ref + sd_other)
        # maj_for_other = ( dist_from_ref.loc[:,bz] - dist_from_other.loc[:,bz] ).mul(wgt, axis = 1).mean(axis = 1)
        
        ref_maj_mean = maj_for_other[b1].mean()
        ref_maj_sd = maj_for_other[b1].std() + 1e-10
        
        sf = (ref_maj_mean)/(ref_maj_sd)
        th_maj = ref_maj_mean + ref_maj_sd*sf
        uc_maj_lower = th_maj - ref_maj_sd*sf*uc_margin
        uc_maj_upper = th_maj + ref_maj_sd*sf*uc_margin
    
        ref_maj_mean = 0
        other_maj_mean = 0
        
        b_stop = True
        
    else:        
        mu_other = X_cnv.loc[b3,:].mean()
        sd_other = X_cnv.loc[b3,:].std()
    
        # zscore = np.abs(mu_ref - mu_other)/(sd_ref + sd_other)
        # bz = zscore >= z_th
        '''
        dist_from_ref = np.abs( X_cnv.sub( mu_ref, axis = 1 )).div(sd_ref, axis = 1 )
        dist_from_other = np.abs( X_cnv.sub( mu_other, axis = 1 )).div(sd_other, axis = 1 )

        maj_for_other = ( dist_from_ref.loc[:,bz] > dist_from_other.loc[:,bz] ).mean(axis = 1)
        '''

        gmm_other = mixture.GaussianMixture(n_components = int(gmm_ncomp_t), covariance_type = 'diag', random_state = 0)
        gmm_other.fit( X_cnv.loc[b3,:] )
        dist_from_other = -gmm_other.score_samples( X_cnv ) ## score_samples: log-likelihood
        dist_from_other = pd.Series(dist_from_other, index = X_cnv.index)
    
        maj_for_other = ( dist_from_ref - dist_from_other ) # .mean(axis = 1)
        
        # wgt = np.abs(mu_ref -mu_other)/(sd_ref + sd_other)
        # maj_for_other = ( dist_from_ref.loc[:,bz] - dist_from_other.loc[:,bz] ).mul(wgt, axis = 1).mean(axis = 1)
        
        ref_maj_mean = maj_for_other[b1].mean()
        ref_maj_sd = maj_for_other[b1].std()
        
        other_maj_mean = maj_for_other[b3].mean()
        other_maj_sd = maj_for_other[b3].std()
        
        sf = (other_maj_mean - ref_maj_mean)/(ref_maj_sd + other_maj_sd)
        th_maj = ref_maj_mean + ref_maj_sd*sf
        uc_maj_lower = th_maj - ref_maj_sd*sf*uc_margin
        uc_maj_upper = th_maj + other_maj_sd*sf*uc_margin

    thresholds = {'th': th_maj, 'lower': uc_maj_lower, 'upper': uc_maj_upper}
    # majority_means = {'normal': ref_maj_mean, 'tumor': other_maj_mean

    return maj_for_other, b_stop, sf, ref_maj_mean, other_maj_mean, thresholds


def get_connectivity_seq( cluster_adj_mat, clust_size, cluster_sel, n_neighbors = 14, 
                          net_search_mode = 'max', verbose = True ):

    cluster_adj_mat_sel = cluster_adj_mat[cluster_sel,:][:,cluster_sel]
    clust_size_sel = list(np.array(clust_size)[cluster_sel])
    
    cluster_adj_mat_nrom = get_normalized_agg_adj_mat( cluster_adj_mat_sel, clust_size_sel, 
                                                       n_neighbors = n_neighbors)
    
    j = cluster_adj_mat_nrom.sum(axis = 1).argmax()
    seed = [j] #  [cluster_sel[j]]
    
    merged_cluster_sel, added_sel, conns_sel = merge_clusters_with_seed( cluster_adj_mat_sel, 
                              clust_size_sel, seed = seed,
                              n_neighbors = n_neighbors,
                              connectivity_thresh = 0.0,  
                              net_search_mode = net_search_mode,
                              verbose = verbose)
    
    merged_cluster_sel = [cluster_sel[j] for j in merged_cluster_sel]
    added_sel = [cluster_sel[j] for j in added_sel]
    
    merged_cluster, added, conns = merge_clusters_with_seed( cluster_adj_mat, clust_size, 
                              seed = cluster_sel, n_neighbors = n_neighbors,
                              connectivity_thresh = 0.0,  
                              net_search_mode = net_search_mode,
                              verbose = verbose)
    
    merged_clusters =  merged_cluster_sel + merged_cluster
    added = added_sel + added
    conns = conns_sel + conns

    return conns, merged_clusters


def calculate_connectivity_threshold( connectivity_seq, no_cluster_sel, wgt = None,
                                      spf = 1/3, sd_mul = 23, conn_th_min = 0.05,
                                      conn_th_max = 0.3 ):

    conns = copy.deepcopy(connectivity_seq)
    
    p2 = int(no_cluster_sel)
    p1 = int(p2*spf)

    # print(p1, p2, len(conns))
    if p2 >= len(conns):
        conns_sel = np.array(conns[p1:])
        p2 = len(conns) - 1
        c_odr = np.arange(p1, len(conns))
    else:
        conns_sel = np.array(conns[p1:p2])
        c_odr = np.arange(p1, p2)
        
    # print(len(c_odr), len(conns_sel))
    z = np.polyfit(c_odr, conns_sel, 1, w = wgt)
    p = np.poly1d(z)

    conns_est = p(c_odr)
    conns_sd = sd_mul*np.sqrt( ((conns_est - conns_sel)**2).mean() )
    
    c_odr = np.arange(len(conns))
    conns_est = p(c_odr)
    
    if p[1] > 0:
        conns_est[:] = np.mean(conns_sel)
    
    conn_th = conns_est[p2] - conns_sd
    # conn_th = conns[p2]
    if conn_th < conn_th_min:
        conn_th = conn_th_min        
        # conns_sd = conns_est[p2] - conn_th
    elif conn_th > conn_th_max:
        conn_th = conn_th_max            

    return conn_th, conns_est, conns_sd


def update_cluster_sel(conns, conn_th, cluster_sel, cluster_seq, spf = 0.1 ):
    
    cluster_sel_new = copy.deepcopy(cluster_sel)
    N_cluster_sel = len(cluster_sel)
    update = 0

    if N_cluster_sel >= len(conns):
        update = 2
        ## No tumor cells
    else:    
        ## Check if any added clusters has connectivity below threshold
        min_conn2 = np.array(conns)[N_cluster_sel:].min()
        min_conn1 = np.array(conns)[int(spf*N_cluster_sel):N_cluster_sel].min()
        
        b = np.array(conns)[N_cluster_sel:] < conn_th
        if min_conn1 > min_conn2: # (np.sum(b) > 3):
            ## use conn_th and cluster_sel as is
            pass
        else:
            ## find the last cluster (in cluster_sel) that has its connectivity below threshold
            '''
            b = np.array(conns) < conn_th
            if np.sum(b) > 0:
                last = np.nonzero(b)[0][-1]
                if last > N_cluster_sel*3/4:
                    for i in range(last):
                        if conns[last-(i+1)] >= conn_th:
                            break
                    
                    cluster_sel_new = cluster_seq[:(last - (i+1))]
                    cluster_sel_new.sort()
                    ## use conn_th as is     
                    update = 1
                else:
                    update = 2      
                    ## No tumor cells
            #'''
            min_conn1_pos = np.array(conns)[int(spf*N_cluster_sel):N_cluster_sel].argmin() + int(spf*N_cluster_sel)
            if min_conn1_pos > N_cluster_sel*(1 - spf):
                last = min_conn1_pos
                for i in range(int(last)):
                    if conns[last-(i+1)] > conn_th:
                        break
                
                cluster_sel_new = cluster_seq[:(last - (i+2))]
                cluster_sel_new.sort()
                ## use conn_th as is     
                update = 1
            else:
                update = 0
                ## Skip
                pass

    return update, conn_th, cluster_sel_new


def inferploidy( X_cnv, X_pca = None, adj_dist = None, ref_ind = None, ## should be provided
                 Clustering_algo = 'lv', Clustering_resolution = 2, 
                 ref_pct_min = 0.2, dec_margin = 0.2, n_neighbors = 14, N_loops = 5, N_runs = 5, 
                 n_cores = 4, connectivity_min = 0.18, connectivity_max = 0.27, 
                 net_search_mode = 'sum', spf = 0.3, connectivity_std_scale_factor = 3, 
                 plot_connection_profile = False, suffix = '', verbose = False, 
                 gmm_ncomp_n = 2, gmm_ncomp_t = 3, 
                 n_pca_comp = 15, use_umap = False, cs_comp_method = 0, cs_ref_quantile = 0, 
                 N_cells_max_for_clustering = 60000, N_cells_max_for_pca = 60000, 
                 N_clusters = 30, clust_labels = None, cnv_score = None ):

    connectivity_thresh_org = connectivity_min
    connectivity_thresh = connectivity_min
    refp_min = ref_pct_min
    
    uc_margin = dec_margin
    N_clusters = find_num_clusters( X_cnv.shape[0], Clustering_resolution )
    if verbose: 
        if (Clustering_algo != 'lv') & (Clustering_algo != 'cc'):
            print('Clustering using %s with N_clusters = %i. ' % (Clustering_algo.upper(), N_clusters))
    
    ## Remove all zero X_cnv
    X_cnv_mean = np.array(X_cnv.sum(axis = 1))
    b = X_cnv_mean == 0
    if np.sum(b) > 0:
        # print(np.sum(b))
        odr = np.array(X_cnv_mean).argsort()
        o_min = odr[int(np.sum(b))]
        x_cnv = X_cnv[o_min,:]
        idxs = np.arange(X_cnv.shape[0])[list(b)]
        for i in idxs:
            X_cnv[i,:] = x_cnv
            
    ref_addon = None
    score_key = 'tumor_score' + suffix
    cluster_key = 'cnv_cluster' 
    
    ##########
    ## PCA ###
    start_time = time.time()
    start_time_a = start_time
    if verbose: 
        print('Running iCNV addon .. ', end = '', flush = True)
    
    if not isinstance(X_cnv, pd.DataFrame):
        X_cnv = pd.DataFrame(X_cnv)
    df = pd.DataFrame(index = X_cnv.index.values)
    
    if X_pca is None: 
        # X_pca = pca_obj.fit_transform(X_cnv)
        X_pca = pca_subsample(X_cnv, N_components_pca = n_pca_comp, 
                              N_cells_max_for_pca = N_cells_max_for_pca)
        
        etime = round(time.time() - start_time) 
        if verbose: print('P(%i) .. ' % etime, end = '', flush = True)
        start_time = time.time()           
    # else: 
    #    X_pca = np.array(X_cnv.copy(deep = True)) #.copy(deep = True)
        
    if use_umap & UMAP_INSTALLED:
        ## Tune some params for umap-based identification
        Clustering_resolution = Clustering_resolution/3
        connectivity_thresh = connectivity_thresh/10
        
        umap_obj = umap.UMAP(random_state=0, n_neighbors = n_neighbors) #, 
                             # precomputed_knn = (neighbors, distances))
        X_vec = umap_obj.fit_transform(X_pca)
        
        etime = round(time.time() - start_time) 
        if verbose: print('U(%i) .. ' % etime, end = '', flush = True)
        start_time = time.time()           
    else: 
        X_vec = np.array(copy.deepcopy(X_pca))   
    
    ## Get neighbor lst and dst    
    clust_labels_all = clust_labels
    # adj_dist = None
    
    if adj_dist is None:
        adj_dist = kneighbors_graph(X_vec, int(n_neighbors), mode = 'distance', # 'connectivity', 
                           include_self=True, n_jobs = 4)
        
    neighbors, distances = get_neighbors(adj_dist, n_neighbors)

    ####################
    #### Outer Loop ####

    uc_lst = {}
    sf_lst = {}
    df_lst = {}
    res_lst = {}
    
    #'''
    if clust_labels_all is None:
        clust_labels_all, cobj, adj_dist = clustering_alg(X_vec, clust_algo = Clustering_algo, 
                                                        N_clusters = N_clusters, 
                                                        resolution = Clustering_resolution, 
                                                        N_neighbors = n_neighbors, 
                                                        n_cores = n_cores, adj_dist = adj_dist)  
    else:
        cobj = None

    etime = round(time.time() - start_time) 
    if verbose: print('A(Nc=%i)(%i) .. ' % (np.max(clust_labels_all)+1, etime), end = '', flush = True)
    start_time = time.time()

    #'''
    #######################
    ## Compute CNV score ##
    if cnv_score is not None:
        y_conf = np.array(cnv_score)*100
    else:
        if cs_comp_method <= 0:
            y_conf = (np.sqrt(X_cnv**2).mean(axis = 1))*100
        else:
            # y_conf = (np.sqrt(X_cnv**2).mean(axis = 1))*100
            q = cs_comp_method
            if q > 0.9: q = 0.9
            sq_X_cnv = X_cnv**2
            qv = sq_X_cnv[sq_X_cnv > 0].quantile(q).quantile(q)
            y_conf = np.log10( ((sq_X_cnv >= qv)).sum(axis = 1) + 1 )
        
    #'''
    
    for orun in range(N_runs):
    
        # if verbose: print('Run: %i ' % orun)
        
        # ref_score = np.array(adata.obsm['cnv_addon_results']['y_conf'])
        cnv_clust_col = cluster_key
        tumor_dec_col = 'tumor_dec'
        score_col = score_key
        ref_ind_col = 'ref_ind'
        
        uc_margin = dec_margin    
        uc_margin_max = 0.4
        if uc_margin > uc_margin_max:
            uc_margin = uc_margin_max
        if N_loops < 2:
            N_loops = 2
        
        a = np.arange(N_loops)
        b = (uc_margin_max-uc_margin)/(N_loops-1)
        uc_margin_lst = uc_margin_max - a*b
            
        ####################
        #### Inner Loop ####
        if orun > 0:
            clust_labels_all, cobj, adj_dist_t = clustering_alg( X_vec, clust_algo = Clustering_algo, 
                                                                N_clusters = N_clusters, 
                                                                resolution = Clustering_resolution, 
                                                                N_neighbors = n_neighbors, 
                                                                n_cores = n_cores, adj_dist = adj_dist,
                                                                random_state = orun)  

            clust_labels_all, cobj, adj_dist_t = clustering_subsample( X_vec, adj_dist, neighbors, distances, 
                                                     clust_labels = clust_labels_all,
                                                     clust_algo = Clustering_algo, N_clusters = N_clusters, 
                                                     resolution = Clustering_resolution, N_neighbors = n_neighbors, 
                                                     n_cores = n_cores,  
                                                     N_cells_max = int(X_vec.shape[0]*0.95) ) # N_cells_max_for_clustering )  

        ## Compute Cluster size, Aggregated Adj.Mat and Merge Small clusters     
        y_clust = copy.deepcopy( clust_labels_all )
        cnv_clust_lst, cluster_size = get_cluster_lst_and_sizes(y_clust)
        
        ## Generate agg_adj_mat
        cluster_adj_mat = get_cluster_adj_mat_from_adj_dist(adj_dist, y_clust)
        
        df_stat = None
        if ref_ind is None: 
            cluster_sel_org = initially_detect_major_clusters( cluster_adj_mat, cluster_size, 
                                             n_neighbors = n_neighbors, connectivity_thresh = connectivity_thresh, 
                                             net_search_mode = net_search_mode, verbose = verbose )
        else:
            cluster_sel_org, df_stat = get_ref_clusters(y_clust, np.array(ref_ind), refp_min, 
                                           ref_score = y_conf, cs_quantile = cs_ref_quantile)
        
        thresholds = []    
        df = pd.DataFrame( index = X_cnv.index )
        df[cnv_clust_col] = list(y_clust)
        df[ref_ind_col] = list(ref_ind)
        df[tumor_dec_col] = 'Normal'
        df[score_col] = 0

        #######################################
        #### Adjust connectivity_threshold ####

        sf = 10
        z_th = 0
        cluster_sel = copy.deepcopy(cluster_sel_org)
        b_stop = False
        ref_ind_tmp = copy.deepcopy(ref_ind)
                
        conns, cluster_seq = get_connectivity_seq( cluster_adj_mat, cluster_size, cluster_sel, n_neighbors, 
                                                      net_search_mode = net_search_mode, verbose = False )
        # conns = medfilt(conns, 5 )
        N_cluster_sel = len(cluster_sel)            
        conn_th, conns_est, conns_sd = calculate_connectivity_threshold( conns, N_cluster_sel, spf = spf, 
                                                                         sd_mul = connectivity_std_scale_factor, 
                                                                         conn_th_min = connectivity_thresh_org,
                                                                         conn_th_max = connectivity_max )
        update = 3
        if False:  # conns_est[0] < conns_est[-1]:
            ## No tumor cells
            print('CT adjust: It seems that no tumor cells exist. (%i) ' % update)
            b_stop = True
            pass
        else:
            update, conn_th_new, cluster_sel_new = update_cluster_sel(conns, conn_th, cluster_sel, cluster_seq, spf = spf)
        
            # display(update)
            if update == 0:
                print('CT adjust: Connectivity threshold: %5.3f, N_cluster_sel: %i ' % \
                      (connectivity_thresh_org, len(cluster_sel_new)))
                connectivity_thresh = conn_th_new
                pass
            elif update == 1:
                print('CT adjust: Connectivity threshold: %5.3f > %5.3f, N_cluster_sel: %i > %i ' % \
                      (connectivity_thresh_org, conn_th, len(cluster_sel), len(cluster_sel_new)))
                connectivity_thresh = conn_th
                cluster_sel = cluster_sel_new
                ref_ind_tmp = np.array( pd.Series(y_clust).isin(cluster_sel) )
            else:
                print('CT adjust: It seems that no tumor cells exist. (%i) ' % update)
                b_stop = True
            
        
        #'''
        if plot_connection_profile:
            plt.figure(figsize = (6,3))
            plt.plot( np.arange(len(conns)), conns )
            plt.grid()
            
            # for x, y in zip(np.arange(len(conns)), conns):
            #     plt.text( x, y, '(%i) %5.3f' % (x,y), fontsize = 5 )

            y_max = np.ceil(np.max(conns)*10)/10
            
            plt.plot( np.arange(len(conns_est)), conns_est )
            plt.plot( np.arange(len(conns_est)), conns_est-conns_sd )
            # plt.plot( np.arange(len(conns_est)), conns_est+conns_sd )
            plt.plot( np.arange(len(conns_est)), [connectivity_thresh]*len(conns_est) )
            plt.plot( [len(cluster_sel)]*19, np.arange(1,20)*y_max/20 )
            plt.text( 3, connectivity_thresh, 'Threshold: %5.3f (std: %4.2f)' % (connectivity_thresh, conns_sd), fontsize = 10 )
            plt.ylabel('Normalized connectivity')
            plt.xlabel('Cluster in connected order')
            plt.ylim( [0, y_max] )
            plt.show()

            # L = N_cluster_sel
            # sd = connectivity_std_scale_factor*np.sqrt( ((conns_est[int(L*0.1):L] - conns[int(L*0.1):L])**2).mean() )
            # print('STD: %4.2f == %4.2f ' % (conns_sd, sd) )
        #'''
        
        #### Adjust connectivity_threshold ####
        #######################################
        
        if b_stop: 
            N_loops = 0
            
        loop_cnt = 0    
        pct_uc = 100
        s_csel = ''
        for crun in range(N_loops):
    
            # start_time = time.time()
            ## Find seed clusters
            df_stat = None
            if crun > 0:
                cluster_sel = None
                refp_min_tmp = refp_min # min( refp_min + crun*0.01, 0.5 )
                if ref_ind_tmp is None: 
                    cluster_sel = initially_detect_major_clusters( cluster_adj_mat, cluster_size, 
                                                                   n_neighbors = n_neighbors, 
                                                                   connectivity_thresh = connectivity_thresh, 
                                                                   net_search_mode = net_search_mode, 
                                                                   verbose = verbose )
                else:
                    cluster_sel, df_stat = get_ref_clusters(y_clust, np.array(ref_ind_tmp), refp_min_tmp, 
                                                   ref_score = y_conf, cs_quantile = cs_ref_quantile)

            ## Find major group of clusters
            merged_cluster, added, connectivities = merge_clusters_with_seed( cluster_adj_mat, cluster_size, 
                                      seed = cluster_sel,
                                      n_neighbors = n_neighbors,
                                      connectivity_thresh = connectivity_thresh, 
                                      net_search_mode = net_search_mode,
                                      verbose = False)

            s_csel = s_csel + '%i-' % len(cluster_sel)
            cluster_added = list(set(merged_cluster) - set(cluster_sel))
            cluster_other = list(set(cnv_clust_lst) - set(merged_cluster))
            
            b0 = (df[cnv_clust_col].astype(int)).isin( cluster_sel_org )
            b1 = (df[cnv_clust_col].astype(int)).isin( cluster_sel )
            b2 = (df[cnv_clust_col].astype(int)).isin( cluster_added )
            b3 = (df[cnv_clust_col].astype(int)).isin( cluster_other )
                    
            maj_for_other, b_stop, sf, ref_maj_mean, other_maj_mean, th_dct = \
                calculate_tumor_score_gmm( X_cnv, b1, b2, b3, uc_margin = uc_margin, z_th = 0,
                                           gmm_ncomp_n = gmm_ncomp_n, gmm_ncomp_t = gmm_ncomp_t )
            
            th_maj = th_dct['th'] 
            uc_maj_lower = th_dct['lower']
            uc_maj_upper = th_dct['upper']
            
            loop_cnt += 1
            thresholds.append((th_maj, uc_maj_lower, uc_maj_upper))    
            
            df[score_col] = list(maj_for_other)

            p_tmp = df[tumor_dec_col].copy(deep = True)
            df[tumor_dec_col] = 'Tumor'                
            if b_stop | (crun == (N_loops - 1)):
                #'''
                b = maj_for_other <= uc_maj_lower 
                df.loc[b&b1, tumor_dec_col] = 'Normal' ######
                b = (maj_for_other < uc_maj_upper) & (maj_for_other > uc_maj_lower)
                df.loc[b&b1, tumor_dec_col] = 'Unclear'
                df.loc[np.array(ref_ind), tumor_dec_col] = 'Normal' ######                
                #''' 
            else:
                df.loc[b1, tumor_dec_col] = 'Normal' ######
                
            b = maj_for_other <= uc_maj_lower 
            df.loc[b&(~b1), tumor_dec_col] = 'Normal'   
            b = (maj_for_other < uc_maj_upper) & (maj_for_other > uc_maj_lower)
            df.loc[b&(~b1), tumor_dec_col] = 'Unclear'

            n_changed = (p_tmp != df[tumor_dec_col]).sum()
        
            df['%s_%i' % (ref_ind_col, crun+1)] = 'Others'
            df.loc[b1, '%s_%i' % (ref_ind_col, crun+1)] = 'Ref'
            df.loc[b2, '%s_%i' % (ref_ind_col, crun+1)] = 'Merged'
            
            # df['%s_%i' % ('ref_ind', crun+1)] = list(ref_ind)
            df['%s_%i' % (score_col, crun+1)] = list(maj_for_other)
            df['%s_%i' % (tumor_dec_col, crun+1)] = df[tumor_dec_col].copy(deep = True)
            
            ref_ind_tmp = (df[tumor_dec_col] == 'Normal') 
            # ref_ind_tmp = df[cnv_clust_col].isin(merged_cluster)
        
            # if verbose: 
            #     print( '   %i SF/UC: %5.3f, %4.2f ' % (crun, sf, pct_uc) )
                
            pct_uc = 100*(df[tumor_dec_col] == 'Unclear').sum()/df.shape[0]
            if b_stop:
                pct_uc = 100
                break   
                
            if n_changed == 0:
                break
        
        #### Inner Loop ####
        ####################
    
        if verbose: 
            if 'ref_maj_mean' not in locals():
                ref_maj_mean = 0
                other_maj_mean = 0

            if not b_stop:
                print( '%i/%i SF/UC/Rm/Tm: %5.3f, %4.2f, %5.3f, %5.3f, C: %s(%i), %i(%i), %i(%i), %i ' % \
                      (orun+1, N_runs, sf, pct_uc, ref_maj_mean, other_maj_mean, 
                       # len(cluster_sel), 
                       s_csel[:-1], np.sum(b1), len(cluster_added), np.sum(b2), 
                       len(cluster_other), np.sum(b3), len(cnv_clust_lst)) )
            else:
                print( '%i/%i SF/UC/Rm/Tm: %5.3f, %4.2f, %5.3f, %5.3f, C: %s(%s), %i(%s), %i(%s), %i ' % \
                      (orun+1, N_runs, sf, pct_uc, ref_maj_mean, other_maj_mean, 
                       # len(cluster_sel), 
                       s_csel[:-1], None, 0, None, 
                       0, None, 0) )

        if df is not None:
            uc_lst[str(orun+1)] = (pct_uc)
            sf_lst[str(orun+1)] = (sf)
            df_lst[str(orun+1)] = (df)
            res_lst[str(orun+1)] = { 'cluster_adj_matrix': cluster_adj_mat,
                                     'TN_decision_thresholds': thresholds,
                                     'TN_t_statistics': sf, 
                                     'unclear_pct': pct_uc,
                                     'tid_summary_df': df }
        
    #### Outer Loop ####
    ####################

    odr = np.array(list(sf_lst.values())).argsort()
    # odr = np.array(uc_lst).argsort()
    o = odr[0]
    key = list(sf_lst.keys())[o]

    df = df_lst[key]
    sf = sf_lst[key]
    pct_uc = uc_lst[key]

    df_t = pd.DataFrame(index = df.index)
    df_s = pd.DataFrame(index = df.index)
    for k in df_lst.keys():
        df_t[k] = list(df_lst[k]['tumor_dec'])
        df_s[k] = list(df_lst[k][score_col])
    
    maj = df_t.mode(axis = 1)
    b = maj[0].isna()
    maj.loc[b,0] = 'Unclear'
    df_t['tumor_dec'] = list(maj[0])
    df_t[score_col] = list(df_s.mean(axis = 1))
    
    if verbose: 
        print( 'Best run: %i with SF/UC: %5.3f, %4.2f ' % (o+1, sf, pct_uc) )
    
    etime = round(time.time() - start_time) 
    if verbose: print('D(%i) .. ' % etime, end = '', flush = True) 

    summary = {}
    summary['connectivity_threshold'] = connectivity_thresh
    summary['selected run'] = key
    summary['run summary'] = res_lst

    etime = round(time.time() - start_time_a) 
    if verbose: print('done (%i) ' % etime) 
        
    return df_t, summary, cobj, X_pca, adj_dist


#######################################
#### MISC for Tumor cell CCI & DEG ####

def generate_hicat_markers_db( mkr_dict, 
                               celltype_origin,
                               taxo_level = 'minor', 
                               species = 'hs',
                               tissue = 'Tumor', 
                               normal_name = 'Normal' ):

    celltype_lst = list(mkr_dict.keys())
    df = pd.DataFrame( columns = ['tissue', 'cell_type_major',
                                  'cell_type_minor', 'cell_type_subset',
                                  'exp', 'markers'], 
                      index = range(len(celltype_lst)) )
    df['tissue'] = tissue
    
    df['cell_type_major'] = celltype_lst
    df['cell_type_minor'] = celltype_lst
    df['cell_type_subset'] = celltype_lst
    df['exp'] = 'pos'
    if taxo_level == 'minor':
        df['cell_type_major'] = celltype_origin
    elif taxo_level == 'subset':
        df['cell_type_major'] = celltype_origin
        df['cell_type_minor'] = celltype_origin

    '''
    b = df['cell_type_major'] == normal_name
    df.loc[~b, 'cell_type_major'] = celltype_origin
    df.loc[~b, 'cell_type_minor'] = celltype_origin
    df.loc[~b, 'cell_type_subset'] = celltype_origin
    '''
    
    for j, key in enumerate(celltype_lst):
        lst = mkr_dict[key]
        lst.sort()
        s = ''
        for m in lst:
            if species.lower()[0] == 'm':
                mkr = m[0] + m[1:].lower()
            else: mkr = m
            s = s + '%s,' % mkr
        s = s[:-1]
        df.loc[j, 'markers'] = s

    return df
    

def get_markers_from_deg( df_dct, ref_col = 'score',  N_mkrs = 30, 
                          nz_pct_test_min = 0.5, nz_pct_ref_max = 0.1,
                          rem_common = True ):
## Get markers from DEG results

    df_deg = df_dct
    mkr_dict = {}
    b = True
    for key in df_deg.keys():
        if ref_col not in list(df_deg[key].columns.values):
            b = False
            break
    
    if not b:
        print('ERROR: %s not found in column name of DEG results.' % ref_col)
        return None

    for key in df_deg.keys():

        g = key.split('_vs_')[0]
        df = df_deg[key].copy(deep = True)
        b1 = df['nz_pct_test'] >= nz_pct_test_min
        b2 = df['nz_pct_ref'] <= nz_pct_ref_max
        df = df.loc[b1&b2, : ]
        df = df.sort_values([ref_col], ascending = False)

        mkr_dict[g] = list(df.iloc[:N_mkrs].index.values)

    ## Remove common markers
    if rem_common:
        lst = list(mkr_dict.keys())
        cmm = []
        for j, k1 in enumerate(lst):
            for i, k2 in enumerate(lst):
                if (k1 != k2) & (j < i):
                    lc = list(set(mkr_dict[k1]).intersection(mkr_dict[k2]))
                    cmm = cmm + lc
        cmm = list(set(cmm))

        for j, k in enumerate(lst):
            mkr_dict[k] = list(set(mkr_dict[k]) - set(cmm))

    return mkr_dict


def find_condition_specific_markers( df_deg_dct, 
                                     col_score = 'score',
                                     n_markers_max = 100,
                                     score_th = 0.25,
                                     pval_cutoff = 0.05,
                                     nz_pct_test_min = 0,
                                     nz_pct_ref_max = 1,
                                     n = 1, verbose = False ):

    s = ''
    df_deg_dct_updated = {}
    for k in df_deg_dct.keys():
        pct_test = df_deg_dct[k]['nz_pct_test']
        pct_ref = df_deg_dct[k]['nz_pct_ref']
        df_deg_dct[k][col_score] = ((pct_test**n)*(1-pct_ref))*(pct_test > pct_ref) # **(1/(n+1))
        b = df_deg_dct[k][col_score] >= score_th
        b = b & (df_deg_dct[k]['pval'] <= pval_cutoff)    
        df_deg_dct_updated[k] = df_deg_dct[k].loc[b,:].copy(deep = True)
        s = s + '   %s (%i -> %i) \n' % (k, len(b), np.sum(b))
        
    if verbose: print('N_markers: \n' + s[:-2])
    
    mkr_dict = get_markers_from_deg( df_deg_dct_updated, N_mkrs = n_markers_max, 
                                     ref_col = col_score,
                                     nz_pct_test_min = nz_pct_test_min,
                                     nz_pct_ref_max = nz_pct_ref_max,
                                     rem_common = False )
    
    s = ''
    for k in mkr_dict.keys():
        s = s + '%s (%i), ' % (k, len(mkr_dict[k]))
    if verbose: print('N_markers_selected: ' + s[:-2])
    
    ## Print results
    mkrs_all = []
    for key in mkr_dict.keys():
        mkr_dict[key].sort()
        lst = mkr_dict[key]
        mkrs_all = mkrs_all + lst
        # if verbose: print('%s (%i): ' % (key, len(lst)), lst)

    return mkr_dict, mkrs_all, df_deg_dct_updated


def find_tumor_origin( adata, tid_col = 'tumor_dec', ref_taxo_level = 'celltype_major' ):
    
    b = adata.obs[tid_col] == 'Tumor'
    pcnt = adata.obs.loc[b, ref_taxo_level].value_counts()
    tumor_origin = [pcnt.index[0]]
    tumor_origin_celltype = pcnt.index[0]
    if (tumor_origin_celltype == 'unassigned'):
        if len(pcnt) > 1:
            if (pcnt[1] >= pcnt[0]*0.05):
                tumor_origin = tumor_origin + [pcnt.index[1]]
                tumor_origin_celltype = pcnt.index[1]
    #'''
    elif len(pcnt) > 1:
        if pcnt.index[1] == 'unassigned':
            tumor_origin = tumor_origin + ['unassigned']
    #'''
    return tumor_origin, tumor_origin_celltype


def set_tumor_info( adata_t, tid_col = 'tumor_dec', 
                     celltype_col = 'celltype_minor',
                     sample_col = 'sample', 
                     cond_col = 'condition', 
                     ref_taxo_level = 'celltype_major',
                     normal_cells = ['Normal', 'Preneoplastic'],
                     adj_normal_name = 'Adj_normal', 
                     tumor_ind_col = 'tumor_origin_ind',
                     cond_specific_adj_normal = True,
                     cond_lst_not_specified = ['Not specified']):  

    colname_suffix = '_for_deg'
    
    # celltype_col = 'celltype_minor'
    if not isinstance(normal_cells, list):
        print('ERROR: normal_cells must be a list.')
        normal_cells = []
        # return

    sample_rev = '%s%s' % (sample_col, colname_suffix)
    cond_rev = '%s%s' % (cond_col, colname_suffix)
    celltype_minor_rev = 'celltype%s' % (colname_suffix)
    '''
    sample_rev = '%s%s' % (sample_col, colname_suffix)
    cond_rev = '%s%s' % (cond_col, colname_suffix)
    celltype_minor_rev = '%s%s' % (celltype_col, colname_suffix)
    '''
    celltype_minor_cci = 'celltype_for_cci' # % (celltype_col)
    
    tumor_origin, org_celltype = find_tumor_origin( adata_t, tid_col, ref_taxo_level )

    adata_t.obs[cond_rev] = adata_t.obs[cond_col].copy(deep = True).astype(str)
    adata_t.obs[sample_rev] = adata_t.obs[sample_col].copy(deep = True).astype(str)
    adata_t.obs[celltype_minor_rev] = adata_t.obs[celltype_col].copy(deep = True).astype(str)
    adata_t.obs[celltype_minor_cci] = adata_t.obs[celltype_col].copy(deep = True).astype(str)
    
    bt = adata_t.obs[tid_col] == 'Tumor'
    bt = bt | (adata_t.obs[ref_taxo_level].isin(tumor_origin))
    adata = adata_t[bt,:]

    adata_t.obs[tumor_ind_col] = False
    adata_t.obs.loc[bt, tumor_ind_col] = True
    
    tlst = list(adata.obs[tid_col].astype(str))
    clst = list(adata.obs[cond_rev].astype(str))
    slst = list(adata.obs[sample_rev].astype(str))
    
    c_new_lst = []
    s_new_lst = []
    ct_new_lst = []
    for t, c, s in zip(tlst, clst, slst):
        if t == 'Tumor':
            if (c in normal_cells) | (c.lower() in normal_cells):
                if (c in cond_lst_not_specified) | (c.lower() in cond_lst_not_specified):
                    c = 'Normal'
                c_new = '%s' % (c) # 'Normal'
                s_new = '%s %s' % (c, s)
                ct_new = 'Normal %s' % org_celltype
            else:
                if (c in cond_lst_not_specified) | (c.lower() in cond_lst_not_specified):
                    c = 'Tumor'
                c_new = '%s' % (c)
                s_new = '%s %s' % (c, s)
                ct_new = 'Tumoric %s' % org_celltype
        elif t == 'Normal':
            if (c in normal_cells) | (c.lower() in normal_cells):
                if (c in cond_lst_not_specified) | (c.lower() in cond_lst_not_specified):
                    c = 'Normal'
                c_new = '%s' % (c) # 'Normal'
                s_new = '%s %s' % (c, s)
                ct_new = 'Normal %s' % org_celltype
            else:
                if (c in cond_lst_not_specified) | (c.lower() in cond_lst_not_specified):
                    c_new = '%s' % (adj_normal_name)
                    s_new = '%s %s' % (adj_normal_name, s)
                else:
                    if cond_specific_adj_normal:
                        c_new = '%s %s' % (adj_normal_name, c)
                    else:
                        c_new = '%s' % (adj_normal_name)                    
                    s_new = '%s %s %s' % (adj_normal_name, c, s)                
                ct_new = '%s %s' % (adj_normal_name, org_celltype)
                
        else:
            c_new = 'Unclear'
            s_new = '%s %s' % (t, s)
            ct_new = 'Unclear %s' % org_celltype
            
        s_new_lst.append(s_new)
        c_new_lst.append(c_new)
        ct_new_lst.append(ct_new)
        
    ilst = adata.obs.index.values.tolist()
    adata_t.obs.loc[ilst, sample_rev] = s_new_lst
    adata_t.obs.loc[ilst, cond_rev] = c_new_lst
    adata_t.obs.loc[ilst, celltype_minor_rev] = org_celltype # ct_new_lst
    adata_t.obs.loc[ilst, celltype_minor_cci] = ct_new_lst
    
    b = adata_t.obs[tumor_ind_col]
    adata = adata_t[b,:]
    
    return org_celltype, adata

