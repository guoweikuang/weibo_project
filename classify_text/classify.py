# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
classify module

@author guoweikuang
"""
import os
import jieba
import pickle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from .config import stop_path
from .config import data_path
from .utils import read_file
from .utils import save_file
from .utils import read_bunch
from .utils import save_bunch
from .utils import remove_and_restart_join
from .utils import classify_result


class Perdict(object):

    def __init__(self, corpus_path, seg_path, bag_path, train_bag_path):
        """
        :param corpus_path:
        :param seg_path:
        :param bag_path:
        """
        self.corpus_path = corpus_path
        self.seg_path = seg_path
        self.bag_path = bag_path
        self.train_bag_path = train_bag_path
        #self.test_bag_path = test_bag_path
        self.bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])

    @property
    def stop_list(self):
        stop = read_file(stop_path).splitlines()
        return stop

    def create_or_exists(self, path):
        """ create file if not exists.

        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def save_seg_content(self):
        """ participle text and save to file.

        :return:
        """
        for path in os.listdir(self.corpus_path):

            category_path = os.path.join(self.corpus_path, path)
            seg_file_path = os.path.join(self.seg_path, path)
            self.create_or_exists(seg_file_path)

            for category in os.listdir(category_path):
                full_path = os.path.join(category_path, category)
                content = read_file(full_path).strip()
                content_seg = jieba.cut(content)
                seg_cate_path = os.path.join(seg_file_path, category)
                save_file(seg_cate_path, ' '.join(content_seg).encode('utf-8'))

    def save_bunch(self, bag_name):
        """

        :return:
        """
        category_list = os.listdir(self.seg_path)
        self.bunch.target_name.extend(category_list)

        for path in category_list:
            category_path = os.path.join(self.seg_path, path)

            for category in os.listdir(category_path):
                full_path = os.path.join(category_path, category)
                self.bunch.label.append(path)
                self.bunch.filenames.append(full_path)
                self.bunch.contents.append(read_file(full_path))

        bag_path = os.path.join(self.bag_path, '%s.dat' % bag_name)
        file = open(bag_path, 'wb')
        pickle.dump(self.bunch, file)
        file.close()

    def tf_idf(self, file_name):
        """

        :param file_name:
        :return:
        """
        path = os.path.join(self.bag_path, '%s.dat' % file_name)
        bunch = read_bunch(path)
        tfidf_space = Bunch(target_name=bunch.target_name, label=bunch.label,
                            filenames=bunch.filenames, tdm=[], vocabulary={})

        vectorizer = TfidfVectorizer(stop_words=self.stop_list, sublinear_tf=True,
                                     max_df=0.5)
        transformer = TfidfTransformer()
        tfidf_space.tdm = vectorizer.fit_transform(bunch.contents)
        tfidf_space.vocabulary = vectorizer.vocabulary_

        space_path = os.path.join(self.bag_path, 'tfidfspace.dat')
        save_bunch(space_path, tfidf_space)

    def test_tf_idf(self, file_name):
        """

        :param file_name:
        :return:
        """
        path = os.path.join(self.bag_path, '%s.dat' % file_name)
        bunch = read_bunch(path)

        test_space = Bunch(target_name=bunch.target_name, label=bunch.label,
                           filenames=bunch.filenames, tdm=[], vocabulary={})
        train_bunch = read_bunch(os.path.join(self.train_bag_path, 'tfidfspace.dat'))

        vectorizer = TfidfVectorizer(stop_words=self.stop_list, sublinear_tf=True,
                                     max_df=0.5, vocabulary=train_bunch.vocabulary)
        transformer = TfidfTransformer()
        test_space.tdm = vectorizer.fit_transform(bunch.contents)
        test_space.vocabulary = train_bunch.vocabulary

        space_path = os.path.join(self.bag_path, 'testspace.dat')
        save_bunch(space_path, test_space)

    def navie_alg(self):
        train_path = os.path.join(self.train_bag_path, 'tfidfspace.dat')
        train_set = read_bunch(train_path)

        test_path = os.path.join(self.bag_path, 'testspace.dat')
        test_set = read_bunch(test_path)
        clf = MultinomialNB(alpha=0.001).fit(train_set.tdm, train_set.label)

        predicted = clf.predict(test_set.tdm)
        total = len(predicted)
        rate = 0
        for flabel, file_name, expct_cate in zip(test_set.label, test_set.filenames, predicted):
            if flabel != expct_cate:
                rate += 1
                print(file_name)
                print("实际类别:" + flabel)
                print("-->预测类别:")
                print(expct_cate)
                print('====' * 40)
                remove_and_restart_join(self.corpus_path, file_name, expct_cate, flabel)
        print("error_rate: ", float(rate) * 100 / float(total))


def run_classify(corpus_path, seg_path, bag_path, test_bag_path, test_corpus_path, test_seg_path):
    #classify = Perdict(corpus_path, seg_path, bag_path, test_bag_path)
    #classify.save_seg_content()
    #classify.save_bunch('train_set')

    #classify.tf_idf(file_name='train_set')

    test_classify = Perdict(test_corpus_path, test_seg_path, test_bag_path, bag_path)
    test_classify.save_seg_content()
    test_classify.save_bunch('test_set')
    test_classify.test_tf_idf(file_name='test_set')
    test_classify.navie_alg()
    classify_result(test_corpus_path, data_path)

