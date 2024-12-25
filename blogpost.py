import subprocess

subprocess.run([
	"curl", "-X", "POST", "-H", "Content-Type: application/json",
	"-d", '{"title":"First Post", "content":"This is the first post content."}',
	"http://127.0.0.1:5000/posts"
])