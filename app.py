
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")

        return f"""
        <h2>Registration Successful!</h2>
        <p>Name: {name}</p>
        <p>Email: {email}</p>
        <a href="/">Register another user</a>
        """

    return """
    <html>
    <head><title>Registration Application</title></head>
    <body>
        <h2>User Registration</h2>
        <form method="POST">
            <label>Name:</label>
            <input type="text" name="name" required><br><br>
            <label>Email:</label>
            <input type="email" name="email" required><br><br>
            <button type="submit">Register</button>
        </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
