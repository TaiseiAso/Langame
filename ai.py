# coding: utf-8


from argparse import ArgumentParser
from torch import optim
import yaml
import random
import torch
import torch.nn as nn
import numpy as np


def get_option(mode, config_path):
    argparser = ArgumentParser()
    argparser.add_argument('-m', '--mode', type=str,
        default=mode, help="Select mode (train or test model).")
    argparser.add_argument('-c', '--config', type=str,
        default=config_path, help="Path of config file.")
    return argparser.parse_args()


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()

    def init_hidden(self, batch_size=1):
        return torch.zeros(self.layer, batch_size, self.hidden)

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        if torch.cuda.is_available():
            self.load_state_dict(torch.load(path))
        else:
            self.load_state_dict(torch.load(path, map_location=lambda storage, loc: storage))


class Encoder(Model):
    def __init__(self, dim, hidden, layer, dropout):
        super().__init__()
        self.dim, self.hidden, self.layer = dim, hidden, layer
        self.embedding = nn.Linear(dim, hidden)
        self.gru = nn.GRU(hidden, hidden, layer, dropout=(0 if layer == 1 else dropout))

    def forward(self, inp, h, batch_size=1):
        inp = inp.view(1, batch_size, self.dim)
        inp = self.embedding(inp)
        _, h = self.gru(inp, h)
        return h


class Decoder(Model):
    def __init__(self, dim, hidden, layer, dropout):
        super().__init__()
        self.dim, self.hidden, self.layer = dim, hidden, layer
        self.embedding = nn.Linear(dim, hidden)
        self.gru = nn.GRU(hidden, hidden, layer, dropout=(0 if layer == 1 else dropout))
        self.output = nn.Linear(hidden, dim)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, inp, h, batch_size=1):
        inp = inp.view(1, batch_size, self.dim)
        inp = self.embedding(inp)
        out, h = self.gru(inp, h)
        out = self.output(out[0])
        out = self.softmax(out)
        return out, h


class AI:
    def __init__(self, config_path):
        self.config = yaml.load(stream=open(config_path, 'rt', encoding='utf-8'), Loader=yaml.SafeLoader)
        self.device = torch.device('cuda:'+str(self.config['cuda']) if torch.cuda.is_available() else 'cpu')
        self.init_dict()

    def init_dict(self):
        self.word_to_id = {}
        self.id_to_word = {}
        for i, order in enumerate(list(range(ord('ぁ'), ord('ん')+1)) + [ord('！'),ord('？'),ord('、'),ord('ー'),ord('_'),ord('>'),ord('$')]):
            self.word_to_id[chr(order)] = i
            self.id_to_word[i] = chr(order)
        self.dim = len(self.word_to_id)

    def load_corpus(self, path):
        use_corpus_size = self.config['train']['use_corpus_size']
        corpus = []
        cnt = 0
        with open(path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                if cnt == use_corpus_size:
                    break
                corpus.append(line.strip())
                cnt += 1
                line = f.readline()
        return corpus

    def init_model(self):
        model = self.config['model']
        self.encoder = Encoder(self.dim, model['hidden'], model['layer'], model['dropout']).to(self.device)
        self.decoder = Decoder(self.dim, model['hidden'], model['layer'], model['dropout']).to(self.device)

    def prepare_test(self):
        self.init_model()
        path = self.config['path']
        self.encoder.load(path['encoder'])
        self.decoder.load(path['decoder'])
        self.encoder.eval()
        self.decoder.eval()

    def padding(self, pairs):
        inp_size_max, tar_size_max = 0, 0
        for pair in pairs:
            if inp_size_max < len(pair[0]):
                inp_size_max = len(pair[0])
            if tar_size_max < len(pair[1]):
                tar_size_max = len(pair[1])

        for i in range(len(pairs)):
            pairs[i][0].extend([self.word_to_id['_']]*(inp_size_max - len(pairs[i][0])))
            pairs[i][0].reverse()
            pads = tar_size_max - len(pairs[i][1])
            pairs[i][1].append(self.word_to_id['$'])
            pairs[i][1].extend([self.word_to_id['_']]*pads)

    def get_batch(self):
        batch_size = self.config['train']['batch_size']
        data_batch = []
        random.shuffle(self.data_pair)
        data_pair_size = len(self.data_pair)
        for i in range(0, data_pair_size, batch_size):
            slice = self.data_pair[i : min([i+batch_size, data_pair_size])]
            self.padding(slice)
            slice_T = np.array(slice).T.tolist()
            data = [np.array(slice_T[0]).T.tolist(), np.array(slice_T[1]).T.tolist()]
            data_batch.append(data)
        random.shuffle(data_batch)
        return data_batch

    def create_mask(self, inp):
        mask = [[0]*self.encoder.hidden if id == self.word_to_id['_'] else [1]*self.encoder.hidden for id in inp]
        return torch.LongTensor([mask for _ in range(self.encoder.layer)])

    def optim_zero_grad(self):
        self.encoder_optim.zero_grad()
        self.decoder_optim.zero_grad()

    def optim_step(self):
        self.encoder_optim.step()
        self.decoder_optim.step()

    def update(self, criterion):
        loss_list = []
        batch = self.get_batch()

        for batch_inp, batch_tar in batch:
            nbatch = len(batch_inp[0])
            self.optim_zero_grad()

            h = self.encoder.init_hidden(nbatch).to(self.device)
            for inp in batch_inp:
                h_ = h
                vec = torch.eye(self.dim)[inp].to(self.device)
                h = self.encoder(vec, h, nbatch)
                mask = self.create_mask(inp).to(self.device)
                h = torch.where(mask == 0, h_, h)

            inp = [self.word_to_id['>']]*nbatch
            loss = 0
            for tar in batch_tar:
                vec = torch.eye(self.dim)[inp].to(self.device)
                out, h = self.decoder(vec, h, nbatch)
                loss += criterion(out, torch.LongTensor(tar).to(self.device))
                inp = tar

            loss.backward()
            self.optim_step()
            loss_list.append(loss.item() / len(batch_tar))

        return sum(loss_list) / len(loss_list)

    def assign_pair(self, inp_data, tar_data):
        return [[[self.word_to_id[word] for word in inp if word in self.word_to_id],
            [self.word_to_id[word] for word in tar if word in self.word_to_id]]
            for (inp, tar) in zip(inp_data, tar_data)]

    def train(self):
        path = self.config['path']
        train_config = self.config['train']
        inp_data = self.load_corpus(path['inp'])
        tar_data = self.load_corpus(path['tar'])

        self.init_model()
        self.encoder.train()
        self.decoder.train()

        self.encoder_optim = optim.Adam(self.encoder.parameters(), lr=train_config['learning_rate'])
        self.decoder_optim = optim.Adam(self.decoder.parameters(), lr=train_config['learning_rate'])
        self.data_pair = self.assign_pair(inp_data, tar_data)

        try:
            for epoch in range(1, train_config['max_epoch']+1):
                print("TRAIN(" + str(epoch-1) + "-" + str(epoch) + "):", end="")
                loss = self.update(nn.NLLLoss(ignore_index=self.word_to_id['_']))
                print(loss)
        except KeyboardInterrupt:
            pass

        self.encoder.save(path['encoder'])
        self.decoder.save(path['decoder'])

    def test(self, inp):
        ids = [self.word_to_id[word] for word in inp if word in self.word_to_id]
        ids.reverse()

        h = self.encoder.init_hidden().to(self.device)
        for id in ids:
            vec = torch.eye(self.dim)[id].to(self.device)
            h = self.encoder(vec, h)

        test_config = self.config['test']
        beam_search = beam_width = test_config['beam_width']
        sequences = [[0, "", self.word_to_id['>'], h, 0]]
        results = []

        for _ in range(test_config['max_length']):
            if beam_search <= 0:
                break
            next_sequences = []

            for score, sentence, id, h, length in sequences:
                vec = torch.eye(self.dim)[id].to(self.device)
                out, h = self.decoder(vec, h)
                topv, topi = out.topk(beam_search)

                for v, i in zip(topv[0], topi[0]):
                    next_id = i.item()
                    word = self.id_to_word[next_id]
                    if word in ['>', '_']:
                        continue
                    elif word == '$':
                        next_setence = sentence
                    else:
                        next_setence = sentence + word
                    next_score = score - v
                    next_length = length + 1
                    next_sequences.append([next_score, next_setence, next_id, h, next_length])

            sequences = sorted(next_sequences)[:beam_search]
            for seq in sequences:
                if seq[2] == self.word_to_id['$']:
                    seq[0] /= seq[4]
                    results.append(seq)
                    beam_search -= 1

            for seq in results:
                if seq in sequences:
                    sequences.remove(seq)

        min_length = test_config['min_length']
        for result in sorted(results)[:beam_width]:
            if len(result[1]) >= min_length:
                return result[1]
        return "？"


if __name__ == '__main__':
    args = get_option('train', 'config/ai_config.yml')
    ai = AI(args.config)
    if args.mode == 'train':
        ai.train()
    else:
        ai.prepare_test()
        while True:
            try:
                user = input("  USER: ")
                res = ai.test(user)
                print("SYSTEM: " + res)
            except KeyboardInterrupt:
                break
