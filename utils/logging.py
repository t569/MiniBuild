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
        with open(dest_file, 'r+') as read_dest:
            try:
                log_buffer.append(json.load(read_dest))

            except:
                # dump something if there is nothing there
                log_buffer.append([])
                json.dump([], read_dest)


        # now read the source file
        with open(source_file, 'r') as read_src:
            try:
                log_buffer.append(json.load(read_src))

            except:
                log_buffer.append([])

        """
        # now combine the source and destination
        # destination can have something in it, should be included to avoid loss of data
        # if source is something then proceed
        """

        # TODO: MODIFY WHAT SHOULD BE LOGGED
        if log_buffer[1]:
            for logs in log_buffer:
                for log in logs:
                    final_log.append(log)

        if final_log:

            with open(dest_file, 'r+') as read_write_dest:
                content = json.load(read_write_dest)
                if final_log != content:
                    # overwrite the file
                    read_write_dest.seek(0)

                    json.dump(final_log, read_write_dest, indent=4)

                    read_write_dest.truncate()










