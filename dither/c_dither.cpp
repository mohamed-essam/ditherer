#include <vector>
#include <stdlib.h>
#include <stdio.h>
#include <utility>
#include <unistd.h>

using namespace std;

int BLEED_THRESHOLD = 90;

struct color{
  int r,g,b;
};

int color_dist(color a, color b){
  return abs(a.r-b.r) + abs(a.g-b.g) + abs(a.b-b.b);
}

color color_error(color a, color b){
  return {a.r-b.r, a.g-b.g, a.b-b.b};
}

color get_color(color c, int* colors, int color_count){
  int minimum_dist = color_dist(c, {colors[0], colors[1], colors[2]});
  int best_index = 0;
  for(int i = 1; i < color_count; i++){
    int dist = color_dist(c, {colors[i*3], colors[i*3+1], colors[i*3+2]});
    if(dist < minimum_dist){
      minimum_dist = dist;
      best_index = i;
    }
  }
  return {colors[best_index*3], colors[best_index*3+1], colors[best_index*3+2]};
}

void add_error(int* forward_array, int i, int j, int error, int width, int height, int forward_index){
  if(i < 0 || j < 0 || i >= height || j >= width) return;
  forward_array[forward_index*width+j] += error;
}

void distribute_error(int i, int j, int* forward_array, int error, int width, int height, int forward_index, int* algorithm, int a_height, int a_offset, int a_divisor){
  for(int k = 0; k < a_height; k++){
    for(int l = -a_offset; l <= a_offset; l++){
      add_error(forward_array, i+k, l+j, (error*algorithm[k*(a_offset*2+1)+l+a_offset]) / a_divisor, width, height, (forward_index+k)%3);
    }
  }
}

extern "C" void dither(int* r, int* g, int* b, int height, int width, int* algorithm, int a_height, int a_offset, int a_divisor, int* colors, int color_count){
  int* forward_array_r = new int[3*width];
  int* forward_array_g = new int[3*width];
  int* forward_array_b = new int[3*width];
  int forward_index = 0;
  for(int i = 0; i < 3*width; i++){
    forward_array_r[i] = forward_array_g[i] = forward_array_b[i] = 0;
  }
  for(int i = 0; i < height; i++){
    for(int j = 0; j < width; j++){
      color s = {r[i*width+j] + forward_array_r[forward_index*width+j], g[i*width+j]+ forward_array_g[forward_index*width+j], b[i*width+j] + forward_array_b[forward_index*width+j]};
      color new_color = get_color(s, colors, color_count);
      color new_error = color_error(s, new_color);
      distribute_error(i, j, forward_array_r, (new_error.r * BLEED_THRESHOLD) / 100, width, height, forward_index, algorithm, a_height, a_offset, a_divisor);
      distribute_error(i, j, forward_array_g, (new_error.g * BLEED_THRESHOLD) / 100, width, height, forward_index, algorithm, a_height, a_offset, a_divisor);
      distribute_error(i, j, forward_array_b, (new_error.b * BLEED_THRESHOLD) / 100, width, height, forward_index, algorithm, a_height, a_offset, a_divisor);
      r[i*width+j] = new_color.r;
      g[i*width+j] = new_color.g;
      b[i*width+j] = new_color.b;
    }
    for(int j = 0; j < width; j++){
      forward_array_r[forward_index*width+j] = forward_array_g[forward_index*width+j] = forward_array_b[forward_index*width+j] = 0;
    }
    forward_index++;
    forward_index%=3;
  }
  delete[] forward_array_r;
  delete[] forward_array_g;
  delete[] forward_array_b;
}

extern "C" void free_memory(int* to_free){
  delete[] to_free;
}
