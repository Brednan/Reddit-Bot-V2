from account import Account


def parse_accounts(path_):
    f = open(path_, 'r')
    file_content = f.read()
    f.close()

    combo_list = file_content.strip().split('\n')
    return combo_list


class Bot:
    def __init__(self, combo_path, vote_type):
        self.FAILED_LOGIN = 0
        self.NO_CONNECTION = 1
        self.SUCCESSFUL_LOGIN = 2

        self.accounts_list = parse_accounts(combo_path)
        self.vote_type = vote_type
