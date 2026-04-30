linguagens = ["python", "js", "c", "java", "csharp"]

# ["c", "js", "java", "python", "csharp"]
print(sorted(linguagens, key=lambda x: len(x)))
# ["python", "csharp", "java", "js", "c"]
print(sorted(linguagens, key=lambda x: len(x), reverse=True))
