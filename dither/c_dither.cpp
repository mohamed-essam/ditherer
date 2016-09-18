#include <vector>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

extern "C" class ditherer{
public:
  vector<vector<int> > color_palette;
  int h, w;
  int forward_index;
  vector<vector<int> > forward_array;
  vector<vector<int> > algorithm;
  int algorithm_divider;
  int algo_offset;
  int index;

  ditherer(){
    index = 0;
    forward_index = 0;
  }

  int color_dist(int r1, int g1, int b1, int r2, int g2, int b2){
    return abs(r1-r2) + abs(g1-g2) + abs(b1-b2);
  }

  int* color_error(int r1, int g1, int b1, int r2, int g2, int b2){
    int* ret = new int[3];
    ret[0] = r1-r2, ret[1] = g1-g2, ret[2] = b1-b2;
    return ret;
  }

  int* get_color(int r, int g, int b){
    int mn = 1e9;
    int best_index = -1;
    for(int i = 0; i < color_palette.size(); i++){
      int dst = color_dist(r,g,b,color_palette[i][0],color_palette[i][1],color_palette[i][2]);
      if(dst < mn){
        mn = dst;
        best_index = i;
      }
    }
    int* ret2 = color_error(r,g,b,color_palette[best_index][0],color_palette[best_index][1],color_palette[best_index][2]);
    int* ret= new int[6];
    ret[0] = ret2[0], ret[1] = ret2[1], ret[2] = ret2[2],
    ret[3] = color_palette[best_index][0],
    ret[4] = color_palette[best_index][1],
    ret[5] = color_palette[best_index][2];
    printf("%d %d %d\n", ret[0], ret[1], ret[2]);
    delete[] ret2;
    return ret;
  }

  void add_error(int i, int j, int error, int fa_i, int h_offset){
    if(i < 0 || j < 0 || i >= h || j >= w){
      return;
    }
    forward_array[fa_i][((forward_index+h_offset)%3)*w+j] += error;
  }

  void add_color_pallete(int r, int g, int b){
    vector<int> tp(3,r);
    tp[1] = g, tp[2] = b;
    color_palette.push_back(tp);
  }

  void distribute_error(int fa_i, int i, int j, int error){
    for(int k = 0; k < algorithm.size(); k++){
      for(int l = -algo_offset; l <= algo_offset; l++){
        add_error(i+k, l+j, (error*algorithm[k][l+algo_offset]) / algorithm_divider, fa_i, k);
      }
    }
  }

  int dither(int r, int g, int b){
    int new_r = r + forward_array[0][forward_index*w+(index%w)];
    int new_g = g + forward_array[1][forward_index*w+(index%w)];
    int new_b = b + forward_array[2][forward_index*w+(index%w)];
    int* color_error = get_color(new_r, new_g, new_b);
    distribute_error(0, index/w, index%w, color_error[0]);
    distribute_error(1, index/w, index%w, color_error[1]);
    distribute_error(2, index/w, index%w, color_error[2]);
    index++;
    if(index%w == 0){
      for(int i = 0; i < 3; i++){
        for(int j = 0; j < algo_offset*2+1; j++){
          forward_array[i][forward_index*w+j] = 0;
        }
      }
      forward_index++;
      forward_index%=3;
    }
    int ret = 0;
    ret += color_error[3];
    ret = ret << 8;
    ret += color_error[4];
    ret = ret << 8;
    ret += color_error[5];
    delete[] color_error;
    return ret;
  }

};

extern "C" ditherer* get_ditherer(int h, int w, int ah, int aw, int div){
  ditherer* ret = new ditherer();
  ret->h=h, ret->w=w;
  ret->algorithm.assign(ah, vector<int>(aw, 0));
  ret->algo_offset = aw/2;
  ret->algorithm_divider = div;
  ret->forward_array.assign(3, vector<int>(3*w, 0));
  printf("%d %d\n", ret->algo_offset, div);
  return ret;
}

extern "C" void put_algorithm_data(int val, int i, int j, ditherer* dith){
  dith->algorithm[i][j] = val;
}

extern "C" void add_color_pallete(int r, int g, int b, ditherer* dith){
  dith->add_color_pallete(r,g,b);
}

extern "C" int dither_color(int r, int g, int b, ditherer* dith){
  return dith -> dither(r,g,b);
}
