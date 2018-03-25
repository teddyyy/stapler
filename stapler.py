# -*- coding: utf-8 -*-

import os
import sys
import yaml
import argparse

from github import Github
from github import GitRelease

# PATH
CONFIG_PATH = './config/'

# token
github_access_token = os.getenv('GITHUB_ACCESS_TOKEN', None)

def unpublish_release(token, yaml):
    g = Github(token)

    for i in range(len(yaml['target'])):
        if yaml['target'][i]['repository'] is not None:
            repository = g.get_user().get_repo(yaml['target'][i]['repository'])
        else:
            print('Empty repository name is not allowed.')
            sys.exit(1)

        # delete existing release
        for release in repository.get_releases():
            if release.tag_name == yaml['release_name']:
                id = release.id
        
        tgt_release = repository.get_release(id)
        tgt_release.delete_release()

        # delete existing tag
        ref = repository.get_git_ref('tags/' + yaml['tag_name'])
        ref.delete()

def publish_release(token, yaml):
    g = Github(token)

    for i in range(len(yaml['target'])):
        if yaml['target'][i]['repository'] is not None:
            repository = g.get_user().get_repo(yaml['target'][i]['repository'])
        else:
            print('Empty repository name is not allowed.')
            sys.exit(1)

        if yaml['target'][i]['branch'] is None:
            branch = repository.get_branch('master')
        else:
            branch = repository.get_branch(yaml['target'][i]['branch'])

        tag = repository.create_git_tag(yaml['tag_name'], yaml['tag_description'], branch.commit.sha, "commit")
        repository.create_git_ref('refs/tags/{}'.format(tag.tag), tag.sha)
        repository.create_git_release(tag.tag, tag.tag, yaml['release_description'])


def load_yaml(path):
    f = open(path, 'r').read()
    ret = yaml.load(f)

    return ret

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--file", type = str, help = "config file name", required = True)
    parser.add_argument('-d', "--delete", action='store_true')
    args = parser.parse_args()

    if github_access_token is None:
        print('Specify GITHUB_ACCESS_TOKEN as environment variable.')
        sys.exit(1)

    yaml = load_yaml(CONFIG_PATH + args.file)
    if yaml['target'] is None:
        print('Specify target repository name.')
        sys.exit(1)

    if (args.delete):
        unpublish_release(github_access_token, yaml)
    else:
        publish_release(github_access_token, yaml)    

if __name__ == '__main__':
    main()