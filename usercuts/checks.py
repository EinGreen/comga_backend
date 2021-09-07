from dbcuts import dbshorts

def check_author(token):
    author_check = dbshorts.run_selection("select u.is_author from users u inner join user_session us on u.id = us.user_id where us.login_token = ?", 
                                          [token,])
    return author_check

def check_user(user_id):
    check = dbshorts.run_selection("select u.id, username, email, image_url from users u inner join user_session us on u.id = us.user_id where us.user_id=?", 
                                   [user_id,])
    return check

def check_session(token):
    login = dbshorts.run_selection("select u.id from users u inner join user_session us on u.id = us.user_id where us.login_token = ?",
                                   [token,])
    return login

#! Might not actually need this: 
# def check_content(content_id):
#     check = dbshorts.run_selection("select c.id from content c where c.id = ?",
#                                    [content_id,])
#     return check

def tag_check(content_id):
    tag_check = dbshorts.run_selection("select c.tags from content c where c.id = ?",
                                       [content_id,])
    return tag_check

