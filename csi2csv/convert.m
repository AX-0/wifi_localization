function convert(base_dir, sub_dir, output_dir)
    % Get a list of iteration directories (0, 1, 2, ..., 9) in the 'dat' folder
    dat_dir = fullfile(base_dir, sub_dir);
    csv_dir = fullfile(base_dir, output_dir);

    % Create the output 'csv' directory if it doesn't exist
    if ~exist(csv_dir, 'dir')
        mkdir(csv_dir);
    end

    iterations = dir(dat_dir);
    iterations = iterations([iterations.isdir] & ~ismember({iterations.name}, {'.', '..'}));
    
    % Loop over each iteration folder
    for iter_idx = 1:length(iterations)
        iter_name = iterations(iter_idx).name;
        iter_input_dir = fullfile(dat_dir, iter_name);
        iter_output_dir = fullfile(csv_dir, iter_name);
        
        % Create the corresponding output directory
        if ~exist(iter_output_dir, 'dir')
            mkdir(iter_output_dir);
        end
        
        % Get a list of .dat files in the current iteration folder
        dat_files = dir(fullfile(iter_input_dir, '*.dat'));
        
        % Process each .dat file
        for file_idx = 1:length(dat_files)
            dat_filename = dat_files(file_idx).name;
            input_filepath = fullfile(iter_input_dir, dat_filename);
            
            % Construct the output CSV filename
            [~, name, ~] = fileparts(dat_filename);
            csv_filename = fullfile(iter_output_dir, [name, '.csv']);
            
            % Convert the .dat file to .csv using the provided function
            csi_to_csv(input_filepath, csv_filename);
        end
    end
end

% convert('../data', '../data/csv');