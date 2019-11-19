# coding: utf-8


import yaml
import os
import json
import re
import time
import unicodedata
import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import MeCab


class QueueListener(StreamListener):
    def __init__(self, api_key, twitter_config):
        super(QueueListener, self).__init__()
        self.queue = []
        self.batch_size = 100
        self.cnt = 0
        cfg_auth = api_key['twitter_API']
        self.auth = OAuthHandler(cfg_auth['consumer_key'], cfg_auth['consumer_secret'])
        self.auth.set_access_token(cfg_auth['access_token'], cfg_auth['access_token_secret'])
        self.api = tweepy.API(self.auth)
        self.path = twitter_config['path']
        self.tagger = MeCab.Tagger('-Ochasen')
        self.tagger.parse("")

    def on_error(self, status):
        print("ON ERROR: ", status)
        return True

    def on_limit(self, track):
        print("ON LIMIT: ", track)
        return

    def on_exception(self, exception):
        print("ON EXCEPTION: ", exception)
        return

    def on_connect(self):
        print("ON CONNECT")
        return

    def on_disconnect(self, notice):
        print("ON DISCONNECT: ", notice.code)
        return

    def on_timeout(self):
        print("ON TIMEOUT")
        return True

    def on_warning(self, notice):
        print("ON WARNING: ", notice.message)
        return

    def on_data(self, data):
        raw = json.loads(data)
        return self.on_status(raw)

    def on_status(self, raw):
        if isinstance(raw.get('in_reply_to_status_id'), int):
            pair = (raw['in_reply_to_status_id'], unicodedata.normalize('NFKC', raw['text']))
            self.queue.append(pair)
            if len(self.queue) >= self.batch_size:
                self.dump()
                print(self.cnt, end=" ", flush=True)
        return True

    def dump(self):
        with open(self.path['inp'], 'a', encoding='utf-8') as f_inp, \
        open(self.path['tar'], 'a', encoding='utf-8') as f_tar:
            (sids, texts), self.queue = zip(*self.queue), []
            while True:
                try:
                    pair_mapper = {s.id_str: s.text for s in self.api.statuses_lookup(sids)}
                    break
                except:
                    time.sleep(10)
            pair_grp = [[unicodedata.normalize('NFKC', pair_mapper.get(str(sid))), text] for sid, text in zip(sids, texts) if pair_mapper.get(str(sid))]
            pair_grp = [[self.del_username(text) for text in pair] for pair in pair_grp]
            for pair in pair_grp:
                if self.check(pair[0]) and self.check(pair[1]):
                    inp = self.del_morpheme(self.normalize(pair[0]))
                    tar = self.del_morpheme(self.normalize(pair[1]))
                    if inp == "" or tar == "":
                        continue
                    if self.check_punctuation(inp) and self.check_punctuation(tar):
                        inp = self.katakana_to_hiragana(self.del_punctuation(inp))
                        tar = self.katakana_to_hiragana(self.del_punctuation(tar))
                        if self.check_length(inp) and self.check_length(tar):
                            f_inp.write(inp + '\n')
                            f_tar.write(tar + '\n')
                            self.cnt += 1

    def del_username(self, text):
        return re.sub("(^|\s)(@|＠)(\w+)", "", text)

    def check(self, text):
        if re.compile("((ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&amp;%@!&#45;\/]))?)").search(text):
            return False
        if re.compile("(?:^|[^ーー゛゜々ヾヽぁ-ヶ一-龠a-zA-Z0-9&_/>]+)[#＃]([ー゛゜々ヾヽぁ-ヶ一-龠a-zA-Z0-9_]*[ー゛゜々ヾヽぁ-ヶ一-龠a-zA-Z]+[ー゛゜々ヾヽぁ-ヶ一-龠a-zA-Z0-9_]*)").search(text):
            return False
        if re.compile("[a-zA-Z0-9]").search(text):
            return False
        return True

    def normalize(self, text):
        text = re.sub("\(.*?\)", " ", text)
        text = re.sub("[^ぁ-んァ-ヶｧ-ｳﾞ一-龠々ー～〜、。！？!?,，.．\r\n]", " ", text)
        text = re.sub("[,，]", "、", text)
        text = re.sub("[．.]", "。", text)
        text = re.sub("〜", "～", text)
        text = re.sub("、(\s*、)+", "、", text)
        text = re.sub("!+", "！", text)
        text = re.sub("！(\s*！)+", "！", text)
        text = re.sub("\?+", "？", text)
        text = re.sub("？(\s*？)+", "？", text)
        text = re.sub("～(\s*～)*|ー(\s*ー)+", "ー", text)
        text = re.sub("\r\n|\n|\r", "。", text)
        text += "。"
        text = re.sub("[、。](\s*[、。])+", "。", text)
        text = re.sub("[。、！](\s*[。、！])+", "！", text)
        text = re.sub("[。、？](\s*[。、？])+", "？", text)
        text = re.sub("、", " 、 ", text)
        text = re.sub("。", " 。 ", text)
        text = re.sub("(、\s*)+", " 、 ", text)
        text = re.sub("！", " ！ ", text)
        text = re.sub("？", " ？ ", text)
        text = re.sub("([、。！？])(\s*ー)+", "\\1", text)
        text = re.sub("^(\s*[。、！？ー]+)+", "", text)
        text = re.sub("(.+?)\\1{3,}", "\\1\\1\\1", text)
        return text

    def del_morpheme(self, text):
        morphemes = ""
        node = self.tagger.parseToNode(text)
        while node:
            feature = node.feature.split(',')
            if feature[0] == "BOS/EOS":
                node = node.next
                continue
            if node.surface not in ["ノ", "ーノ", "ロ", "艸", "屮", "罒", "灬", "彡", "ヮ", "益",\
            "皿", "タヒ", "厂", "厂厂", "啞", "卍", "ノノ", "ノノノ", "ノシ", "ノツ",\
            "癶", "癶癶", "乁", "乁厂", "マ", "んご", "んゴ", "ンゴ", "にき", "ニキ", "ナカ", "み", "ミ",\
            "笑", "泣"]:
                if len(feature) >= 8:
                    morphemes += feature[7]
                else:
                    morphemes += node.surface
            node = node.next
        return morphemes.strip()

    def check_punctuation(self, text):
        cnt = text.count('。')
        return cnt == 0 or (cnt == 1 and text[-1] == '。')

    def del_punctuation(self, text):
        return re.sub("。", "", text)

    def katakana_to_hiragana(self, text):
        if text == "":
            return ""
        text_ = ""
        i = 0
        while True:
            if 'ァ' <= text[i] <= 'ン':
                text_ += chr(ord(text[i]) - 96)
            elif text[i] == 'ヴ':
                if i < len(text)-1 and 'ァ' <= text[i+1] <= 'ォ':
                    i += 1
                    text_ += chr(ord('ば') + 3*((ord(text[i]) - ord('ァ'))//2))
                else:
                    text_ += 'ブ'
            elif 'ぁ' <= text[i] <= 'ん' or text[i] in ['！','？','、','ー']:
                text_ += text[i]
            else:
                return ""
            i += 1
            if i == len(text):
                break
        return text_

    def check_length(self, text):
        return 3 <= len(text) <= 15


if __name__ == '__main__':
    tcpip_delay = 0.25
    api_key = yaml.load(stream=open("api_key.yml", 'rt', encoding='utf-8'), Loader=yaml.SafeLoader)
    twitter_config = yaml.load(stream=open("twitter_config.yml", 'rt', encoding='utf-8'), Loader=yaml.SafeLoader)
    while True:
        try:
            listener = QueueListener(api_key, twitter_config)
            stream = Stream(listener.auth, listener)
            stream.filter(languages=["ja"], track=['。', '、', '！', '？', '私', '俺', '(', ')'])
        except KeyboardInterrupt:
            stream.disconnect()
            break
        except:
            time.sleep(min(tcpip_delay, 16))
            tcpip_delay += 0.25
