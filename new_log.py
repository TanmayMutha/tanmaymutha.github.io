from datetime import datetime

title = input("Title: ")

now = datetime.now()

entry = f"""
<div class="post">

    <h2>{title}</h2>

    <p class="timestamp">
        {now.strftime("%B %d, %Y %H:%M")}
    </p>

    <p>
        Write here...
    </p>

</div>
"""

print("\n\nCopy this into logs.html:\n")
print(entry)