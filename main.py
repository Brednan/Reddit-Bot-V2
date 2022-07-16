from bot import Bot


if __name__ == '__main__':
    try:
        vote_type = input('Specify vote type | <U> for Upvote and <D> for Downvote: ').lower()

        bot = Bot('./burner_accounts.txt')

    except FileNotFoundError:
        print('\nUnable to locate accounts list!\n')
