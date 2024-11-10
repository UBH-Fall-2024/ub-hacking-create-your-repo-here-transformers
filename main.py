import prompt
import persist

question = input("Enter your question - \n")
persist.persist_data(question)
result = prompt.prompt(question=question)

print(result)
