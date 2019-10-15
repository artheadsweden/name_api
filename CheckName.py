from nameinfo import NameInfo


def main():
    name = input("Please enter your first name: ")
    name_info = NameInfo(name)
    print(name_info.get_predicted_age())
    print(name_info.get_predicted_gender())
    print(name_info)


if __name__ == '__main__':
    main()
