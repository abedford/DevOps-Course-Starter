from flask import session

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    return session.get('items', _DEFAULT_ITEMS)


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    print(items)
    return next((item for item in items if int(item['id']) == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to update.
    """
    existing_items = get_items()
    
    updated_items = [item if int(item['id']) == int(existing_item['id']) else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

def remove_item_by_id(item_id):
    """
    Deletes an existing item in the session that matches the id. If there is no matching existing item, nothing is deleted.

    Args:
    """
    existing_item = get_item(item_id)
        item_id: The id of the item to remove.
    existing_items = get_items()
    if (existing_item != None):
        existing_items.remove(existing_item)
    session['items'] = existing_items
    

    return item_id
