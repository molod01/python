import json

def main():
    j = json.load(open("file.json"))
    print(type(j), j)
    # print(json.dumps(j, indent = 4))
    for i in j:
        print(j[i])
    print()
    for v in j.values():
        print(v)
    print()
    for key, value in j.items():
        print(key, value)

    
    print([i for i in j.values()])


if __name__ == "__main__":
    main()