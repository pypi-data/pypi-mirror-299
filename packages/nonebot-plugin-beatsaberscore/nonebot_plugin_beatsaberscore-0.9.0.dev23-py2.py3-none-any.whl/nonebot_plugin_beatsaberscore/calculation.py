def contrast(new_id_data,new_pp_data,old_id_data,old_pp_data):
    for old_id in old_id_data:
        change_pp_data = []
        count = 0
        song_position = 1
        if count > len(new_id_data):
            change_pp_data.append(song_position)
        else:
            if old_id in new_id_data[count]:
                pass
            else:
                pass
        count += 1
        song_position += 1
