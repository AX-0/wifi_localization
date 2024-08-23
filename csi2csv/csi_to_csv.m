% This MATLAB scripts translates the content of the .dat file read using the Atheros-CSI-Tool-UserSpace-APP
% to a .csv file. It is specifically written for data sent/recevied from devices with 56 subcarriers and 2 antennas.
function csi_to_csv(log_filename, csv_filename)
    % Read the log file with the read_log_file function
    csi_data = read_log_file(log_filename);
    
    % Prepare to collect data for CSV output
    num_records = length(csi_data);
    total_entries = num_records * 56; % Each record has 56 subcarriers***
    records = cell(total_entries, 21); % Adjust size based on the number of columns

    % Initialize entry counter
    entry_counter = 1;

    % Loop through each record and extract required fields
    for i = 1:num_records
        csi_matrix = csi_data{i};
        
        % Extract subcarriers amplitude and phase
        csi = csi_matrix.csi;
        if csi_matrix.csi_len > 0
            csi_amplitude = abs(csi);
            csi_phase = angle(csi);
        else
            csi_amplitude = NaN(56, 2); % 56 subcarriers and 2 antennas
            csi_phase = NaN(56, 2); % 56 subcarriers and 2 antennas
        end
        
        % Loop through each subcarrier
        for subcarrier = 1:56
            % Fill in the record
            records{entry_counter, 1} = csi_matrix.timestamp;
            records{entry_counter, 2} = csi_matrix.csi_len;
            records{entry_counter, 3} = csi_matrix.channel;
            records{entry_counter, 4} = csi_matrix.err_info;
            records{entry_counter, 5} = csi_matrix.noise_floor;
            records{entry_counter, 6} = csi_matrix.Rate;
            records{entry_counter, 7} = csi_matrix.bandWidth;
            records{entry_counter, 8} = csi_matrix.num_tones;
            records{entry_counter, 9} = csi_matrix.nr;
            records{entry_counter, 10} = csi_matrix.nc;
            records{entry_counter, 11} = csi_matrix.rssi;
            records{entry_counter, 12} = csi_matrix.rssi1;
            records{entry_counter, 13} = csi_matrix.rssi2;
            records{entry_counter, 14} = csi_matrix.rssi3;
            records{entry_counter, 15} = csi_matrix.payload_len;
            records{entry_counter, 16} = csi_matrix.csi_len + 2 + 8 + 2 + 2 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + csi_matrix.payload_len;
            records{entry_counter, 17} = subcarrier; % Subcarrier number

            % fprintf("rate: %d\n", csi_matrix.Rate);
            
            if csi_matrix.csi_len > 0
                % fprintf("\n sub: %d\n", subcarrier);
                % fprintf("entry: %d\n", entry_counter);
                % fprintf("amplitude1: %d\n", csi_amplitude(1, 3));
                % fprintf("amplitude2: %d\n", csi_amplitude(2, 3));
                records{entry_counter, 18} = csi_amplitude(1, subcarrier); % Antenna 1 amplitude
                records{entry_counter, 19} = csi_amplitude(2, subcarrier); % Antenna 2 amplitude
                records{entry_counter, 20} = csi_phase(1, subcarrier); % Antenna 1 phase
                records{entry_counter, 21} = csi_phase(2, subcarrier); % Antenna 2 phase
            else
                records{entry_counter, 18} = NaN;
                records{entry_counter, 19} = NaN;
                records{entry_counter, 20} = NaN;
                records{entry_counter, 21} = NaN;
            end
            
            % Increment the entry counter
            entry_counter = entry_counter + 1;
        end
    end
    
    % Convert to table
    column_names = {'timestamps', 'csi_len', 'channel', 'err_info', 'noise_floor', 'rate', 'bandWidth', 'num_tones', 'nr', 'nc', 'rssi', 'rssi1', 'rssi2', 'rssi3', 'payload_length', 'block_length', 'subcarriers', 'ant1_amplitude', 'ant2_amplitude', 'ant1_phase', 'ant2_phase'};
    T = cell2table(records, 'VariableNames', column_names);
    
    % Write the table to a CSV file
    writetable(T, csv_filename);
end