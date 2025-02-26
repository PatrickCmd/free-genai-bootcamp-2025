import json
from .schema import validate_words, validate_groups, validate_word_groups
from .database import get_connection, get_group_id, get_last_group_id, get_last_word_id, get_last_word_group_id

def import_words(file_content):
    """
    Import words from a JSON file into the database
    
    Args:
        file_content (str): JSON file content
        
    Returns:
        tuple: (imported_count, errors)
    """
    try:
        data = json.loads(file_content)
        validated_words = validate_words(data)
        
        # Get database connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get the last word ID to avoid conflicts
        cursor.execute("SELECT MAX(id) as max_id FROM words")
        result = cursor.fetchone()
        last_id = result['max_id'] or 0
        
        # Track imported words
        imported_count = 0
        errors = []
        
        for word in validated_words:
            word_dict = word.model_dump()
            
            # Check if word already exists
            cursor.execute(
                "SELECT id FROM words WHERE jamaican_patois = ? AND english = ?", 
                (word_dict['jamaican_patois'], word_dict['english'])
            )
            existing = cursor.fetchone()
            
            if existing:
                # Word already exists, update it
                try:
                    cursor.execute(
                        """
                        UPDATE words 
                        SET type = ?, usage = ? 
                        WHERE id = ?
                        """,
                        (
                            word_dict['parts']['type'],
                            word_dict['parts'].get('usage', ''),
                            existing['id']
                        )
                    )
                    imported_count += 1
                except Exception as e:
                    errors.append(f"Error updating word {word_dict['jamaican_patois']}: {str(e)}")
            else:
                # New word, insert it
                try:
                    # Use the word's ID if provided, otherwise generate a new one
                    word_id = word_dict.get('id')
                    if word_id is None or word_id <= last_id:
                        last_id += 1
                        word_id = last_id
                    else:
                        last_id = word_id
                    
                    cursor.execute(
                        """
                        INSERT INTO words (id, jamaican_patois, english, type, usage)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            word_id,
                            word_dict['jamaican_patois'],
                            word_dict['english'],
                            word_dict['parts']['type'],
                            word_dict['parts'].get('usage', '')
                        )
                    )
                    imported_count += 1
                except Exception as e:
                    errors.append(f"Error inserting word {word_dict['jamaican_patois']}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        return imported_count, errors if errors else None
    except Exception as e:
        return 0, str(e)

def import_groups(file_content):
    """
    Import groups from a JSON file into the database
    
    Args:
        file_content (str): JSON file content
        
    Returns:
        tuple: (imported_count, errors)
    """
    try:
        data = json.loads(file_content)
        validated_groups = validate_groups(data)
        
        # Get database connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get the last group ID to avoid conflicts
        cursor.execute("SELECT MAX(id) as max_id FROM groups")
        result = cursor.fetchone()
        last_id = result['max_id'] or 0
        
        # Track imported groups
        imported_count = 0
        errors = []
        
        for group in validated_groups:
            group_dict = group.model_dump()
            
            # Check if group already exists
            cursor.execute("SELECT id FROM groups WHERE name = ?", (group_dict['name'],))
            existing = cursor.fetchone()
            
            if existing:
                # Group already exists, nothing to update
                imported_count += 1
            else:
                # New group, insert it
                try:
                    # Use the group's ID if provided, otherwise generate a new one
                    group_id = group_dict.get('id')
                    if group_id is None or group_id <= last_id:
                        last_id += 1
                        group_id = last_id
                    else:
                        last_id = group_id
                    
                    cursor.execute(
                        "INSERT INTO groups (id, name) VALUES (?, ?)",
                        (group_id, group_dict['name'])
                    )
                    imported_count += 1
                except Exception as e:
                    errors.append(f"Error inserting group {group_dict['name']}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        return imported_count, errors if errors else None
    except Exception as e:
        return 0, str(e)

def import_word_groups(file_content):
    """
    Import word-group associations from a JSON file into the database
    
    Args:
        file_content (str): JSON file content
        
    Returns:
        tuple: (imported_count, errors)
    """
    try:
        data = json.loads(file_content)
        validated_word_groups = validate_word_groups(data)
        
        # Get database connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get the last word_group ID to avoid conflicts
        cursor.execute("SELECT MAX(id) as max_id FROM word_groups")
        result = cursor.fetchone()
        last_id = result['max_id'] or 0
        
        # Track imported associations
        imported_count = 0
        errors = []
        
        for word_group in validated_word_groups:
            word_group_dict = word_group.model_dump()
            
            # Check if association already exists
            cursor.execute(
                "SELECT id FROM word_groups WHERE word_id = ? AND group_id = ?", 
                (word_group_dict['word_id'], word_group_dict['group_id'])
            )
            existing = cursor.fetchone()
            
            if existing:
                # Association already exists, nothing to update
                imported_count += 1
            else:
                # New association, insert it
                try:
                    # Check if word and group exist
                    cursor.execute("SELECT id FROM words WHERE id = ?", (word_group_dict['word_id'],))
                    word_exists = cursor.fetchone()
                    
                    cursor.execute("SELECT id FROM groups WHERE id = ?", (word_group_dict['group_id'],))
                    group_exists = cursor.fetchone()
                    
                    if not word_exists:
                        errors.append(f"Word with ID {word_group_dict['word_id']} does not exist")
                        continue
                    
                    if not group_exists:
                        errors.append(f"Group with ID {word_group_dict['group_id']} does not exist")
                        continue
                    
                    # Use the association's ID if provided, otherwise generate a new one
                    assoc_id = word_group_dict.get('id')
                    if assoc_id is None or assoc_id <= last_id:
                        last_id += 1
                        assoc_id = last_id
                    else:
                        last_id = assoc_id
                    
                    cursor.execute(
                        "INSERT INTO word_groups (id, word_id, group_id) VALUES (?, ?, ?)",
                        (assoc_id, word_group_dict['word_id'], word_group_dict['group_id'])
                    )
                    imported_count += 1
                except Exception as e:
                    errors.append(f"Error inserting association: {str(e)}")
        
        conn.commit()
        conn.close()
        
        return imported_count, errors if errors else None
    except Exception as e:
        return 0, str(e)

def get_preview_data(file_content, data_type):
    """
    Get a preview of the data in a JSON file
    
    Args:
        file_content (str): JSON file content
        data_type (str): Type of data ('words', 'groups', or 'word_groups')
        
    Returns:
        tuple: (preview_data, count, errors)
    """
    try:
        data = json.loads(file_content)
        
        if data_type == 'words':
            validated_data = validate_words(data)
            preview = [item.model_dump() for item in validated_data[:5]]  # Show first 5 items
        elif data_type == 'groups':
            validated_data = validate_groups(data)
            preview = [item.model_dump() for item in validated_data[:5]]
        elif data_type == 'word_groups':
            validated_data = validate_word_groups(data)
            preview = [item.model_dump() for item in validated_data[:5]]
        else:
            return None, 0, "Invalid data type"
        
        return preview, len(validated_data), None
    except Exception as e:
        return None, 0, str(e) 