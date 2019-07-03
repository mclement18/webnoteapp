import flask
app = flask.Flask("noteapp")

def get_html(page):
    html_page = open(page + ".html")
    content = html_page.read()
    html_page.close()
    return content

def get_db_content():
        database = open("notesdb.txt")
        content = database.read()
        database.close()
        return content

def write_db(note):
    database = open("notesdb.txt", "a")
    database.write(note + "\n")
    database.close()

def delete_notes_from_db(notes_to_delete):
    db_content = get_db_content()
    for note in notes_to_delete:
        db_content = db_content.replace(note + "\n", "")
    new_db = open("notesdb.txt", "w")
    new_db.write(db_content)
    new_db.close()

def clear_db():
    database = open("notesdb.txt", "w")
    database.close()

def get_notes():
    db_content = get_db_content()
    notes = db_content.split("\n")
    non_empty_note = []
    for note in notes:
        if note:
            non_empty_note.append(note)
    return non_empty_note

def write_note_html(note):
    note_title, note_content = note.split("|")
    note_html = '  <div class="note">\n    <h3 class="note-title">{}</h3>\n    <p class="note-content">{}</p>\n  </div>\n'.format(note_title, note_content)
    return note_html

def get_search_hits(query, notes, where):
    hits = []
    if query:
        for note in notes:
            title_note, content_note = note.split("|")
            if where == "Title" and query.upper() in title_note.upper():
                hits.append(note)
            elif where == "Content" and query.upper() in content_note.upper():
                hits.append(note)
    subtitle = '  <div>\n    <h2>{} hits</h2>\n  </div>\n'.format(where)
    hits_html = ""
    if hits:
        for hit in hits:
            hits_html += write_note_html(hit)
    else:
        hits_html = '  <div class="note">\n    <p class="not_found">No hit found</p>\n  </div>\n'
    return subtitle + hits_html

#Need JavaScript
@app.route("/")
def home():
    return get_html("index")

@app.route("/options")
def options():
    html_page = get_html("options")
    db_content = get_db_content().strip()
    if db_content:
        message = "You have some notes."
    else:
        message = "You don't have note."
    return html_page.replace("$$$INFO$$$", message)
      

@app.route("/add", methods=["POST"])
def add():
    html_page = get_html("options")
    note_title = flask.request.form["title"].strip()
    note_content = flask.request.form["content"].strip()
    if not note_title and not note_content:
        return html_page.replace("$$$INFO$$$", "Empty notes cannot be saved!")
    else:
        note = "|".join([note_title, note_content])
        write_db(note)
        return html_page.replace("$$$INFO$$$", "Note saved!")


@app.route("/notes")
def notes():
    html_page = get_html("notes")
    subtitle = '<div>\n    <h2>All Notes</h2>\n  </div>\n'
    notes = get_notes()
    notes_html = ""
    for note in notes:
        notes_html += write_note_html(note)
    if not notes_html:
        notes_html = "<div><p>You have no note.</p></div>"
    html_output = subtitle + notes_html
    return html_page.replace("$$$NOTES$$$", html_output)


@app.route("/search")
def search():
    html_page = get_html("notes")
    query_title = flask.request.args.get("title")
    query_content = flask.request.args.get("content")
    search = '<div>\n    <h2>Your search:</h2>\ntitlecontent  </div>\n'
    notes = get_notes()
    if query_title:
        title_hits = get_search_hits(query_title, notes, "Title")
        search = search.replace("title", '    <h3 class="search">Title:</h3><p class="search">{}</p>\n'.format(query_title))
    else:
        title_hits = ""
        search = search.replace("title", "")
    if query_content:
        content_hits = get_search_hits(query_content, notes, "Content")
        search = search.replace("content", '    <h3 class="search">Content:</h3><p class="search">{}</p>\n'.format(query_content))
    else:
        content_hits = ""
        search = search.replace("content", "")
    html_output = search + title_hits + content_hits
    return html_page.replace("$$$NOTES$$$", html_output)

# Need JavaScript
# First testing functions using get methods by inputing notes in url
# @app.route("/delete")
# def delete():
#     html_page = get_html("options")
#     notes_to_delete = flask.request.args.get("notes")
#     notes_to_delete_list = notes_to_delete.split("\n")
#     delete_notes_from_db(notes_to_delete_list)
#     message = "Notes deleted."
#     return html_page.replace("$$$INFO$$$", message)
@app.route("/delete", methods=["POST"])
def delete():
    html_page = get_html("options")
    notes_to_delete = flask.request.form["notesToDelete"].strip()
    print(notes_to_delete)
    notes_to_delete_list = notes_to_delete.split("\r\n")
    print(notes_to_delete_list)
    delete_notes_from_db(notes_to_delete_list)
    message = "Notes deleted."
    return html_page.replace("$$$INFO$$$", message)


@app.route("/clear")
def clear():
    html_page = get_html("index")
    clear_db()
    return flask.redirect(flask.url_for('home'))
    
