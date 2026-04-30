linguagens = ["python", "js", "c", "java", "csharp"]
linguagens.sort()  # ["c", "csharp", "java", "js", "python"]
print(linguagens)

linguagens = ["python", "js", "c", "java", "csharp"]
linguagens.sort(reverse=True)  # ["python", "js", "java", "csharp", "c"]
print(linguagens)

linguagens = ["python", "js", "c", "java", "csharp"]
# ["c", "js", "java", "python", "csharp"]
linguagens.sort(key=lambda x: len(x))
print(linguagens)

linguagens = ["python", "js", "c", "java", "csharp"]
# ["python", "csharp", "java", "js", "c"]
linguagens.sort(key=lambda x: len(x), reverse=True)
print(linguagens)
