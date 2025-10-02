def process_entities(annotations_list):
    # print(annotations_list)
    old_type = ''
    annotation = []
    for item in annotations_list:
        start, end, type_token = item

        if type_token == 'O':
            old_type = type_token
            annotation.append((start, end, type_token))

        elif old_type == '':
            type_token = 'B-'+type_token[2:]
            old_type = type_token
            annotation.append((start, end, type_token))

        elif old_type[2:] == type_token[2:]:
            type_token = 'I-'+type_token[2:]
            old_type = type_token
            annotation.append((start, end, type_token))

        elif old_type[2:] != type_token[2:]:
            type_token = 'B-'+type_token[2:]
            old_type = type_token
            annotation.append((start, end, type_token))
        else:
            print('ELSE')

    return annotation