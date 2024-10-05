import numpy as np
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scelda.models import distribute, featurize, load_scelda, load_slda, shuffle, sceLDA, SLDA
from scelda.sim import make_datasets

def test_load_slda(name='tests/slda'):
    ref_model = SLDA()
    ref_model.save(name)
    test_model = load_slda(name)
    assert test_model == ref_model

def test_load_scelda(name='tests/scelda'):
    ref_model = sceLDA()
    ref_model.save(name)
    test_model = load_scelda(name)
    assert test_model == ref_model

def test_featurize(n_samples=100, n_features=1000, scale=1.):
    ref_data = np.hstack([np.ones((n_samples, 1)), np.random.random((n_samples, n_features))])
    test_data = featurize(ref_data, scale)
    assert test_data.shape == (n_samples, n_features - 2)

def test_distribute(n_docs=150):
    locs = make_datasets('chblocks', 1)[0][:, :3]
    doc_locs, doc_vars = distribute(locs, n_docs)
    assert doc_locs.shape == (n_docs, locs.shape[1])
    assert doc_vars.shape == (n_docs,)
    assert locs[:, -2].min() <= doc_locs[:, -2].min() <= doc_locs[:, -2].max() <= locs[:, -2].max()
    assert locs[:, -1].min() <= doc_locs[:, -1].min() <= doc_locs[:, -1].max() <= locs[:, -1].max()

def test_shuffle(n_samples=100, n_topics=10, n_docs=150, n_words=15):
    words = np.hstack([np.arange(n_words).repeat(n_samples//n_words), np.arange(n_samples%n_words)])
    docs, topics, doc_counts, topic_counts = shuffle(words, n_topics, n_docs, n_words, True)
    assert docs.shape == topics.shape == (n_samples, 1)
    assert doc_counts.shape == (n_docs, n_topics)
    assert topic_counts.shape == (n_topics, n_words)
    assert doc_counts.sum() == topic_counts.sum() == n_samples

def test_SLDA_eq():
    model1 = SLDA()
    model2 = SLDA()
    assert model1 == model2

def test_SLDA_neq():
    model1 = SLDA(n_topics=1)
    model2 = SLDA(n_topics=2)
    assert model1 != model2

def test_SLDA_build(n_samples=1000, n_features=100, n_topics=10, n_steps=10):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics).build(data, n_steps)
    assert model.corpus.shape == (n_samples, 6)
    assert model.topics.shape == (n_steps, n_samples)
    assert model.probs.shape == (n_steps, n_samples, n_topics)

def test_SLDA_decrement(n_samples=1000, n_features=100, n_topics=10, n_steps=10, word=0, doc=0, topic=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics).build(data, n_steps)
    ref_doc_counts, ref_topic_counts = model.doc_counts.copy(), model.topic_counts.copy()
    model.decrement(word, doc, topic)
    test_doc_counts, test_topic_counts = model.doc_counts, model.topic_counts
    assert test_doc_counts[doc, topic] == ref_doc_counts[doc, topic] - 1
    assert test_topic_counts[topic, word] == ref_topic_counts[topic, word] - 1

def test_SLDA_increment(n_samples=1000, n_features=100, n_topics=10, n_steps=10, word=0, doc=0, topic=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics).build(data, n_steps)
    ref_doc_counts, ref_topic_counts = model.doc_counts.copy(), model.topic_counts.copy()
    model.increment(word, doc, topic)
    test_doc_counts, test_topic_counts = model.doc_counts, model.topic_counts
    assert test_doc_counts[doc, topic] == ref_doc_counts[doc, topic] + 1
    assert test_topic_counts[topic, word] == ref_topic_counts[topic, word] + 1

def test_SLDA_sample_doc(n_samples=1000, n_features=100, n_topics=10, n_docs=150, n_steps=10, loc=np.arange(3), topic=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics, n_docs).build(data, n_steps)
    doc, probs = model.sample_doc(loc, topic, True)
    assert type(doc) == int
    assert 0 <= doc <= n_docs
    assert probs.shape == (n_docs,)

def test_SLDA_sample_topic(n_samples=1000, n_features=100, n_topics=10, n_steps=10, word=0, doc=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics).build(data, n_steps)
    topic, probs = model.sample_topic(word, doc, True)
    assert type(topic) == int
    assert 0 <= topic <= n_topics
    assert probs.shape == (n_topics,)

def test_SLDA_sample(n_samples=1000, n_features=100, n_topics=10, n_docs=150, n_steps=10, loc=np.arange(3), word=0, doc=0, topic=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics, n_docs).build(data, n_steps)
    doc, topic, likelihood = model.sample(0, 0, loc, word, doc, topic, True)
    assert type(doc) == int
    assert type(topic) == int
    assert 0 <= doc <= n_docs
    assert 0 <= topic <= n_topics
    assert likelihood > 0.

def test_SLDA_update(n_samples=1000, n_features=100, n_topics=10, n_docs=150, n_steps=10, sample=0, step=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics, n_docs).build(data, n_steps)
    model.update(sample, step)
    corpus, topics = model.corpus, model.topics
    doc_counts, topic_counts = model.doc_counts, model.topic_counts
    assert 0 <= corpus[sample, -2] <= n_docs
    assert 0 <= corpus[sample, -1] == topics[sample, step] <= n_topics
    assert doc_counts.sum() == topic_counts.sum() == n_samples

def test_SLDA_step(n_samples=1000, n_features=100, n_topics=10, n_steps=10, step=0):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics).build(data, n_steps)
    likelihood = model.step(step)
    assert likelihood > 0.

def test_SLDA_fit(n_samples=1000, n_features=100, n_topics=10, n_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics).fit(data, n_steps, burn_in, verbosity=0)
    assert len(model.likelihood_log) == n_steps

def test_SLDA_transform(n_samples=1000, n_features=100, n_topics=10, n_steps=10, burn_in=5):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = SLDA(n_topics).fit(data, n_steps, burn_in, verbosity=0)
    topics = model.transform(data)
    assert topics.shape == (n_samples,)
    assert 0 <= topics.min() <= topics.max() <= n_topics

def test_sceLDA_fit(n_samples=1000, n_features=100, n_topics=10, layers=(10,), n_vae_steps=10, n_slda_steps=10, burn_in=5, learning_rate=1e-6):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = sceLDA(n_topics, layers=layers).fit(data, n_vae_steps, n_slda_steps, burn_in, learning_rate, verbosity=0)
    assert len(model.vae.train_log) == len(model.vae.test_log) == n_vae_steps
    assert len(model.slda.likelihood_log) == n_slda_steps

def test_sceLDA_transform(n_samples=1000, n_features=100, n_topics=10, layers=(10,), n_vae_steps=10, n_slda_steps=10, burn_in=5, learning_rate=1e-6):
    locs = np.hstack([np.zeros((n_samples, 1)), np.arange(n_samples*2).reshape(n_samples, 2)])
    features = np.arange(n_samples*n_features).reshape(n_samples, n_features)/(n_samples*n_features)
    data = np.hstack([locs, features])
    model = sceLDA(n_topics, layers=layers).fit(data, n_vae_steps, n_slda_steps, burn_in, learning_rate, verbosity=0)
    topics = model.transform(data)
    assert topics.shape == (n_samples,)
    assert 0 <= topics.min() <= topics.max() <= n_topics
