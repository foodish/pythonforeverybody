#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-28 14:30:13
# @Author  : xxfood
# @Email   : xbj1900@gmail.com
# @Link    : https://foodish.github.io
import sqlite3

conn = sqlite3.connect('xqfriends_0504.db')
cur = conn.cursor()


class SolutionFound(RuntimeError):

    def __init__(self, message):
        self.message = message


def getLinks(fromId):
    # 给定用户id获取其关注列表，result为list
    cur.execute("SELECT to_id FROM Follows WHERE from_id = ?", (fromId,))
    if cur.rowcount == 0:
        return None
    else:
        return [x[0] for x in cur.fetchall()]


def constructDict(currentId):
    # 将当前用户关注列表转为字典形式，形如{1: {}, 2: {}, 3: {}, 4: {}}
    users = getLinks(currentId)
    if users:
        return dict(zip(users, [{}] * len(users)))
    return {}
    # 关注列表要么为空，要么包含多个用户


def searchDepth(targetId, currentId, linkTree, depth):
    """[summary]

    [description]

    Arguments:
        targetId {[int]} -- [目标id]
        currentId {[int]} -- [起始id]
        linkTree {[dict]} -- [关注列表链接树]
        depth {[type]} -- [搜索深度]

    Returns:
        [dict] -- [关系链上的每个id]

    Raises:
        SolutionFound -- [找到链接树]
    """
    cur.execute("SELECT name FROM People WHERE id = ?", (currentId,))
    current_Name = cur.fetchone()  # tuple形式
    currentName = current_Name[0]

    cur.execute("SELECT name FROM People WHERE id = ?", (targetId,))
    target_Name = cur.fetchone()  # tuple形式
    targetName = target_Name[0]

    if depth == 0:
        # 停止递归，返回结果
        return linkTree
    if not linkTree:
        linkTree = constructDict(currentId)
    if not linkTree:
        # 若此用户未关注任何用户，则跳过此节点
        return {}
    if targetId in linkTree.keys():
        # print("TARGET " + str(targetId) + " FOUND!")
        print("TARGET " + str(targetName) + " FOUND!")
        # raise SolutionFound("User: " + str(currentId))
        raise SolutionFound("User: " + str(currentName))

    for branchKey, branchValue in linkTree.items():
        try:
            # 递归建立链接树
            linkTree[branchKey] = searchDepth(targetId, branchKey,
                                              branchValue, depth - 1)
        except SolutionFound as e:
            print(e.message)
            # raise SolutionFound("User: " + str(currentId))
            raise SolutionFound("User: " + str(currentName))

    return linkTree


if __name__ == '__main__':
    targetName = '红色番茄酱'
    fromName = '不明真相的群众'

    cur.execute("SELECT id FROM People WHERE name = ?", (fromName,))
    from_Id = cur.fetchone()  # tuple形式
    currentId = from_Id[0]

    cur.execute("SELECT id FROM People WHERE name = ?", (targetName,))
    target_Id = cur.fetchone()  # tuple形式
    targetId = target_Id[0]

    linkTree = {}
    depth = 4

    try:
        searchDepth(targetId, currentId, linkTree, depth)
        print("No solution found")
    except SolutionFound as e:
        print(e.message)
