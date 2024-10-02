"""Code to test the auditory toolbox."""
from absl.testing import absltest
import jax.numpy as jnp
import numpy as np  # For testing
import scipy
import matplotlib.pyplot as plt

import auditory_toolbox_jax as pat


class AuditoryToolboxTests(absltest.TestCase):
  """Test cases for auditory toolbox."""
  def test_erb_space(self):
    low_freq = 100.0
    high_freq = 44100/4.0
    num_channels = 100
    cf_array = pat.ErbSpace(low_freq = low_freq, high_freq = high_freq,
                           n = num_channels)
    self.assertLen(cf_array, num_channels)
    # Make sure low and high CF's are where we expect them to be.
    self.assertAlmostEqual(cf_array[-1], low_freq, delta=0.001)
    self.assertLess(cf_array[0], high_freq)

  def test_make_erb_filters(self):
    # Ten channel ERB Filterbank.  Make sure return has the right size.
    # Will test coefficients when we test the filterbank.
    fs = 16000
    low_freq = 100
    num_chan = 10
    fcoefs = pat.MakeErbFilters(fs, num_chan, low_freq)
    self.assertLen(fcoefs, 10)

    # Test all the filter coefficient array shapes
    a0, a11, a12, a13, a14, a2, b0, b1, b2, gain = fcoefs
    self.assertEqual(a0.shape, (num_chan,))
    self.assertEqual(a11.shape, (num_chan,))
    self.assertEqual(a12.shape, (num_chan,))
    self.assertEqual(a13.shape, (num_chan,))
    self.assertEqual(a14.shape, (num_chan,))
    self.assertEqual(a2.shape, (num_chan,))
    self.assertEqual(b0.shape, (num_chan,))
    self.assertEqual(b1.shape, (num_chan,))
    self.assertEqual(b2.shape, (num_chan,))
    self.assertEqual(gain.shape, (num_chan,))


  def test_erb_filterbank(self):
    fs = 16000
    low_freq = 100
    num_chan = 10
    fcoefs = pat.MakeErbFilters(fs, num_chan, low_freq)

    impulse_len = 512
    x = jnp.hstack((jnp.ones(1), jnp.zeros(impulse_len-1)))

    y = pat.ErbFilterBank(x, fcoefs)
    self.assertEqual(y.shape, (num_chan, impulse_len))
    self.assertAlmostEqual(np.max(y), 0.10657410, delta=0.01)

    resp = 20*jnp.log10(jnp.abs(jnp.fft.fft(y.T, axis=0)))

    # Test to make sure spectral peaks are in the right place for each channel
    matlab_peak_locs = [184, 132, 94, 66, 46, 32, 21, 14, 8, 4]
    python_peak_locs = jnp.argmax(resp[:impulse_len//2], axis=0)

    # Add one to python locs because Matlab arrays start at 1
    self.assertEqual(matlab_peak_locs, list(python_peak_locs+1))

    # Test using a single array for the fcoefs
    fcoefs_array = jnp.stack(fcoefs)
    self.assertEqual(fcoefs_array.shape, (10, 10))
    y = pat.ErbFilterBank(x, fcoefs)
    self.assertEqual(y.shape, (num_chan, impulse_len))
    self.assertAlmostEqual(np.max(y), 0.10657410, delta=0.01)

  def test_erb_filterbank_example(self):
    """Just to make sure the example code keeps working."""
    n = 512
    fs = 16000
    fcoefs = pat.MakeErbFilters(16000,10,100)
    y = pat.ErbFilterBank(jnp.array([1.0] + [0] * (n-1), dtype=float), fcoefs)
    resp = 20*jnp.log10(jnp.abs(jnp.fft.fft(y, axis=1))).T
    freq_scale = jnp.expand_dims(jnp.linspace(0, 16000, 512), 1)
    plt.semilogx(freq_scale[:n//2, :], resp[:n//2, :])
    plt.axis((100, fs/2, -60, 0))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Filter Response (dB)')

  def test_correlogram_array(self):
    def local_peaks(x):
      i = np.argwhere(np.logical_and(x[:-2] < x[1:-1],
                                    x[2:] < x[1:-1])) + 1
      return [j[0] for j in i]

    test_impulses = jnp.zeros((1,1024))
    for i in range(0, test_impulses.shape[1], 100):
      test_impulses = test_impulses.at[:, i].set(1)
    test_frame = pat.CorrelogramFrame(test_impulses, 256)
    self.assertEqual(list(jnp.where(test_frame > 0.1)[1]),
                      [0, 100, 200])

    # Now test with cochlear input to correlogram
    impulse_len = 512
    fs = 16000
    low_freq = 100
    num_chan = 64
    fcoefs = pat.MakeErbFilters(fs, num_chan, low_freq)

    # Make harmonic input signal
    s = 0
    pitch_lag = 200
    for h in range(1, 10):
      s = s + jnp.sin(2*jnp.pi*jnp.arange(impulse_len)/pitch_lag*h)

    y = pat.ErbFilterBank(s, fcoefs)
    frame_width = 256
    frame = pat.CorrelogramFrame(y, frame_width)
    self.assertEqual(frame.shape, (num_chan, frame_width))
    self.assertGreaterEqual(jnp.min(frame), 0.0)

     # Make sure the top channels have no output.
    spectral_profile = np.sum(frame, 1)
    no_output = np.where(spectral_profile < 2)
    np.testing.assert_equal(no_output[0], np.arange(31))

    # Make sure we have spectral peaks at the right locations
    spectral_peaks = local_peaks(spectral_profile)
    self.assertEqual(spectral_peaks, [42, 44, 46, 48, 50, 53, 56, 60])

    # Make sure the first peak (after 0 lag) is at the pitch lag
    summary_correlogram = jnp.sum(frame, 0)
    skip_lags = 100
    self.assertEqual(np.argmax(summary_correlogram[skip_lags:]) + skip_lags,
                     pitch_lag)

  def test_correlogram_pitch(self):
    sample_len = 20000
    sample_rate = 22254
    pitch_center = 120
    u = pat.MakeVowel(sample_len, pat.FMPoints(sample_len, pitch_center),
                      sample_rate, 'u')

    low_freq = 60
    num_chan = 100
    fcoefs = pat.MakeErbFilters(sample_rate, num_chan, low_freq)
    coch = pat.ErbFilterBank(u, fcoefs)
    cor = pat.CorrelogramArray(coch,sample_rate,50,256)
    [pitch,sal] = pat.CorrelogramPitch(cor, 256, sample_rate,100,200)

    # Make sure center and overall pitch deviation are as expected.
    self.assertAlmostEqual(jnp.mean(pitch), pitch_center, delta=2)
    self.assertAlmostEqual(jnp.min(pitch), pitch_center-6, delta=2)
    self.assertAlmostEqual(jnp.max(pitch), pitch_center+6, delta=2)
    np.testing.assert_array_less(0.8, sal[:40])

    # Now test salience when we add noise
    n = np.random.randn(sample_len) * np.arange(sample_len)/sample_len
    un=u + n/4

    low_freq = 60
    num_chan = 100
    fcoefs = pat.MakeErbFilters(sample_rate, num_chan, low_freq)
    coch= pat.ErbFilterBank(un, fcoefs)
    cor = pat.CorrelogramArray(coch,sample_rate,50,256)
    [pitch,sal] = pat.CorrelogramPitch(cor,256,22254,100,200)

    lr = scipy.stats.linregress(range(len(sal)), y=sal, alternative='less')
    self.assertAlmostEqual(lr.slope, -0.012, delta=0.01)  # Probabilistic data,
    self.assertAlmostEqual(lr.rvalue, -0.963, delta=0.03) # so be tolerant.

  def test_mfcc(self):
    # Put a tone into MFCC and make sure it's in the right
    # spot in the reconstruction.
    sample_rate = 16000.0
    f0 = 2000
    tone = jnp.sin(2*jnp.pi*f0*jnp.arange(4000)/sample_rate)
    [_,_,_,_,freqrecon]= pat.Mfcc(tone,sample_rate,100)

    fft_size = 512  # From the MFCC source code
    self.assertEqual(f0/sample_rate*fft_size,
                     jnp.argmax(jnp.sum(freqrecon, axis=1)))

  def test_fm_points  (self):
    base_pitch = 160
    sample_rate = 16000
    fmfreq = 10
    fmamp = 20
    points = pat.FMPoints(100000, base_pitch, fmfreq, fmamp, 16000)

    # Make sure the average glottal pulse locations is 1 over the pitch
    d_points = points[1:] - points[:-1]
    self.assertAlmostEqual(jnp.mean(d_points), sample_rate/base_pitch, delta=1)

    # Make sure the frequency deviation is as expected.
    # ToDo(malcolm): Test the deviation, it's not right!

  def test_make_vowel(self):
    def local_peaks(x):
      i = jnp.argwhere(jnp.logical_and(x[:-2] < x[1:-1],
                                    x[2:] < x[1:-1])) + 1
      return jnp.array([j[0] for j in i])

    test_seq = local_peaks(jnp.array([1,2,3,2,1,1,2,2,3,4,1]))
    self.assertEqual(list(test_seq), [2, 9])

    def vowel_peaks(vowel):
      """Synthesize a vowel and find the frequencies of the spectral peaks"""
      sample_rate = 16000
      vowel = pat.MakeVowel(1024, [1,], sample_rate, vowel)
      spectrum = 20*jnp.log10(jnp.abs(jnp.fft.fft(vowel)))
      freqs = jnp.arange(len(vowel))*sample_rate/len(vowel)
      return freqs[local_peaks(spectrum)[:3]]

    def peak_widths(vowel, bw=50):
      """Synthesize a vowel and find the frequencies of the spectral peaks"""
      sample_rate = 16000
      vowel = pat.MakeVowel(1024, [1,], sample_rate, vowel, bw=bw)
      spectrum = 20*np.log10(np.abs(np.fft.fft(vowel)))
      peak_locs = local_peaks(spectrum)[:3]
      peak_widths = scipy.signal.peak_widths(spectrum, peak_locs,
                                             rel_height=0.5)[0]
      return peak_widths

    # Make sure the spectrum of each vowel has peaks in the right spots.
    bin_width = 16000/1024
    np.testing.assert_allclose(vowel_peaks('a'),
                               np.array([730, 1090, 2440]),
                               atol=bin_width)
    np.testing.assert_allclose(vowel_peaks('i'),
                               np.array([270, 2290, 3010]),
                               atol=bin_width)
    np.testing.assert_allclose(vowel_peaks('u'),
                               np.array([300, 870, 2240]),
                               atol=bin_width)

    widths_50 = peak_widths('/a/', 50)
    widths_100 = peak_widths('/a/', 100)
    np.testing.assert_array_less(widths_50, widths_100)


if __name__ == '__main__':
  absltest.main()
