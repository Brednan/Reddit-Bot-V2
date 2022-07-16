from account import Account
import threading


def parse_accounts(path_):
    f = open(path_, 'r')
    file_content = f.read()
    f.close()

    combo_list = file_content.strip().split('\n')
    return combo_list


class Bot:
    def __init__(self, combo_path, vote_type, max_threads):
        self.FAILED_LOGIN = 0
        self.NO_CONNECTION = 1
        self.SUCCESSFUL_LOGIN = 2

        self.accounts_list = parse_accounts(combo_path)
        self.vote_type = vote_type

        self.max_threads = max_threads

    def bot_sequence(self):
        c = 0

        while c < len(self.accounts_list):
            if threading.active_count() < self.max_threads:
                credentials = self.accounts_list[c].split(':')

                account = Account(credentials[0], credentials[1])

                if self.vote_type == 'd':
                    threading.Thread(target=self.downvote_sequence, args=(account,)).start()

    def downvote_sequence(self, account):
        login_result = account.login_request(5)

        if login_result == self.SUCCESSFUL_LOGIN:
            pass
