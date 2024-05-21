import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = 'wumao learning 555'

def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_conn()
    post = conn.execute('select * from posts where id = ?', (post_id,)).fetchone()
    return post

@app.route('/')
def index():
    conn = get_db_conn()
    posts = conn.execute("select * from posts order by created desc").fetchall()
    return render_template("index.html", posts=posts)


@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('标题不能为空')
        elif not content:
            flash('内容不能为空')
        else:
            conn = get_db_conn()
            conn.execute('insert into posts (title, content) values (?, ?)', 
                         (title, content))
            conn.commit()
            conn.close()
            flash('文章保存成功')
            return redirect(url_for('index'))
        
    return render_template('new.html')

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    post = get_post(post_id=post_id)
    print(f"{post['title']}, {post['content']}")

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        print(content)
        conn = get_db_conn()
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                     (title, content, post_id))
        conn.commit()
        conn.close()
        flash('修改保存成功')
        return redirect(url_for('index'))
    
    return render_template('edit.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=['DELETE'])
def delete(post_id):
    post = get_post(post_id)
    conn = get_db_conn()
    conn.execute("DELETE FROM post WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" 删除成功!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
