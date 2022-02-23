if __name__ == "__main__":
    repository = "data"
    files = ["toto", "abc", "efg"]
    pattern = ".yaml"

    message = """
        When building the hash config file
            - Function called: hashing.get_hash_config()

        Within the file 'data/verification/hash_config.yaml'
            - This pattern has been defined: {pattern}

        No files found that match the search pattern
            - Pattern: {pattern}

            - Repository: {repository}
            - Files: {files}

        To resolve this warning, please:
            - Edit the file: 'data/verification/hash_config.yaml'
    """.format(
        repository=repository,
        files=files,
        pattern=pattern,
    )

    print(message)
