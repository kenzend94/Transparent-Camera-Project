%% MAE
% Simple MATLAB script to calculate the MAE of two images.
% You could do this in Python but its really easy to do in MATLAB.
%
% Author: Kenneth Gordon
% Date: April 26, 2024

groundTruthImage = imread('environment2_front_599.jpg');
synthesizedImage = imread('environment2_side_599_synthesized_image.jpg');

MAE = sum(abs(synthesizedImage(:)-groundTruthImage(:)))/numel(synthesizedImage)