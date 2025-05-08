import numpy as np


def merge(subset, min_num_body_parts=5, min_score=0.4):
    """
    Estimates the skeletons.
    :param connections: valid connections
    :param min_num_body_parts: minimum number of body parts for a skeleton
    :param min_score: minimum score value for the skeleton
    :return: list of skeletons. Each skeleton has a list of identifiers of body parts:
        [
            [id1, id2,...,idN, score, parts_num],
            [id1, id2,...,idN, score, parts_num]
            ...
        ]

    position meaning:
        [   [nose       , neck           , right_shoulder , right_elbow      , right_wrist  , left_shoulder
             left_elbow , left_wrist     , right_hip      , right_knee       , right_ankle  , left_hip
             left_knee  , left_ankle     , right_eye      , left_eye         , right_ear    , left_ear
             score, parts_num],
        ]
    """

    # 2 step :
    #---merge----
    # Merge the limbs in the subset
    # score : score
    # parts_num : How many limbs are in the subset 
    ###############################
    delete_idx = []

    # 遍歷 subset 中的每個骨架子集，將相互重疊的部分合併
    for i in range(len(subset)):
        for j in range(i + 1, len(subset)):
            # 檢查是否有相同的部位 (即如果某一部位在兩個子集中都存在)
            common_parts = [part for part in range(len(subset[i]) - 2) 
                            if subset[i][part] >= 0 and subset[i][part] == subset[j][part]]
            
            if len(common_parts) > 0:  # 如果有重疊的部分
                for k in range(len(subset[i]) - 2):  # 遍歷所有關節
                    if subset[i][k] < 0 and subset[j][k] >= 0:  # 若 i 缺少某關節但 j 有該關節
                        subset[i][k] = subset[j][k]
                # 合併總分數和部件數量
                subset[i][-2] += subset[j][-2]  # 合併分數
                subset[i][-1] += subset[j][-1]  # 合併部件數
                delete_idx.append(j)  # 記錄需要刪除的索引
    
    # after merge
    #---delete---
    # Delete the non-compliant subset
    # 1. parts_num < 5
    # 2. Average score(score / parts_num) < 0.4 
    ############################################
    for i in range(len(subset)):
        if subset[i][-1] < min_num_body_parts or (subset[i][-2] / subset[i][-1]) < min_score:
            delete_idx.append(i)
    
    subset = np.delete(subset, delete_idx, axis=0)

    print("subset:")
    print(subset)

    return subset    

