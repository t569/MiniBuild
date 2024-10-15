# check if we are lazy loading
# if we are lazy loading, simply open in append mode
# if we are not
# open the file compare the results and log and make the changes

# create a json file called log.json
import json


def log_to_file(source_file, dest_file, lazyLoadTag):
    log_buffer: list[list] = []
    final_log: list = []
    writeFlag: bool = True
    # this is the most difficult
    if lazyLoadTag:

        # read the destination file
        with open(dest_file, 'r') as read_dest:
            try:
                log_buffer.append(json.load(read_dest))

            except:     # error handling
                log_buffer.append([])


        # now read the source file
        with open(source_file, 'r') as read_src:
            try:
                log_buffer.append(json.load(read_src))

            except:
                log_buffer.append([])


        # now combine the source and destination
        # destination can have something in it, should be included to avoid loss of data
        # if source is something then proceed

        # TODO: FIX THIS LOGGING SYSTEM
        if log_buffer[1]:
            for logs in log_buffer:
                for log in logs:
                    final_log.append(log)


        if final_log:
            # check if final_log is the same as the value in the file
            try:
                with open(dest_file, 'r') as read_dest:
                    writeFlag = not (final_log == json.load(read_dest))

            except:
                writeFlag = True # there is nothing in the file, go ahead


        if writeFlag:
            # now if final_log is something we should overwrite the current file
            with open(dest_file, 'w') as dest_write:
                json.dump(final_log, dest_write)









