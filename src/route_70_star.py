"""

@author: Gerardo Cervantes
"""

from load_NN import run_splitter



def get_70_star_split_numbers():
    #Star numbers where it will split
    fade_out_splits = []
    
    #Stars where it should split immediately after grabbing the star
    immediate_splits = [10,13,17,19,24,30,34,39,42,48,52,58,62,69]
    
    return fade_out_splits, immediate_splits
    
def run_auto_splitter(immediate_splits, fade_out_splits, starting_star_number):
    model_path = '../models/High_acc_model_205_imgs_30epochs.hdf5'
    #Sets coordinates to screenshot for pil, should be set to cover the game screen
    x, y, width, height = 61, 82, 615, 449
    
    
    #split key used to split
    split_key = '{PGUP}'
    reset_key = '{PGDN}'
    
    run_splitter(model_path, starting_star_number, split_key, reset_key, fade_out_splits, immediate_splits, x, y, width, height)

if __name__ == "__main__":
    fade_out_splits, immediate_splits = get_70_star_split_numbers()
    starting_star_number = 0
    run_auto_splitter(immediate_splits, fade_out_splits, starting_star_number)



