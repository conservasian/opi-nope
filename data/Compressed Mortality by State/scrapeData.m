% scrapeData.m

clear; clc; close all;

fid = fopen('Compressed Mortality State, 2016.txt');
C = textscan(fid, '%s%d%d%f32', 'Headerlines', 1);
fclose(fid);