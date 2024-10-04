from __future__ import division
from __future__ import absolute_import
from builtins import zip
from builtins import range
from builtins import object
import pytest
from numpy.testing import assert_array_almost_equal
from .test_helpers import (make_1d_traj, data_filename, assert_items_equal,
                           assert_same_items)

import openpathsampling as paths
import openpathsampling.engines as peng
import numpy as np
import os

from openpathsampling.analysis.shooting_point_analysis import *

import logging
logging.getLogger('openpathsampling.initialization').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.storage').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.netcdfplus').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.ensemble').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.engines').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.pathmover').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.sample').setLevel(logging.CRITICAL)


class TestTransformedDict(object):
    def setup_method(self):
        self.untransformed = {(0, 1): "a", (1, 2): "b", (2, 3): "c"}
        self.transformed = {0: "a", 1: "b", 2: "c"}
        self.hash_function = lambda x: x[0]
        self.empty = TransformedDict(self.hash_function, {})
        self.test_dict = TransformedDict(self.hash_function,
                                         self.untransformed)

    def test_initialization(self):
        assert self.test_dict.store == self.transformed
        assert (self.test_dict.hash_representatives ==
                {0: (0, 1), 1: (1, 2), 2: (2, 3)})

    def test_set_get(self):
        self.empty[(5, 6)] = "d"
        assert self.empty.store == {5: "d"}
        assert self.empty.hash_representatives == {5: (5, 6)}
        assert self.empty[(5, 6)] == "d"

    def test_update(self):
        self.test_dict.update({(5, 6): "d"})
        assert self.test_dict.store == {0: "a", 1: "b", 2: "c", 5: "d"}
        assert (self.test_dict.hash_representatives ==
                {0: (0, 1), 1: (1, 2), 2: (2, 3), 5: (5, 6)})

    def test_del(self):
        del self.test_dict[(0, 1)]
        assert self.test_dict.store == {1: "b", 2: "c"}

    def test_iter(self):
        iterated = [k for k in self.test_dict]
        for (truth, beauty) in zip(list(self.untransformed.keys()), iterated):
            assert truth == beauty

    def test_len(self):
        assert len(self.test_dict) == 3
        assert len(self.empty) == 0

    def test_rehash(self):
        rehashed = self.test_dict.rehash(lambda x: x[1])
        assert rehashed.store == {1: "a", 2: "b", 3: "c"}
        assert (rehashed.hash_representatives ==
                {1: (0, 1), 2: (1, 2), 3: (2, 3)})


class TestSnapshotByCoordinateDict(object):
    def setup_method(self):
        self.empty_dict = SnapshotByCoordinateDict()
        coords_A = np.array([[0.0, 0.0]])
        coords_B = np.array([[1.0, 1.0]])
        self.key_A = coords_A.tobytes()
        self.key_B = coords_B.tobytes()
        self.snapA1 = peng.toy.Snapshot(coordinates=coords_A,
                                        velocities=np.array([[0.0, 0.0]]))
        self.snapA2 = peng.toy.Snapshot(coordinates=coords_A,
                                        velocities=np.array([[1.0, 1.0]]))
        self.snapB1 = peng.toy.Snapshot(coordinates=coords_B,
                                        velocities=np.array([[0.0, 0.0]]))
        self.dict1 = SnapshotByCoordinateDict({self.snapA1: "A1",
                                               self.snapB1: "B1"})

    def test_initialization(self):
        assert self.dict1.store == {self.key_A: "A1", self.key_B: "B1"}

    def test_get_set(self):
        self.dict1[self.snapA2] = "A2"
        assert self.dict1.store == {self.key_A: "A2", self.key_B: "B1"}


class TestShootingPointAnalysis(object):
    def setup_method(self):
        self.HAS_TQDM = paths.progress.HAS_TQDM
        paths.progress.HAS_TQDM = False
        # taken from the TestCommittorSimulation
        import openpathsampling.engines.toy as toys
        pes = toys.LinearSlope(m=[0.0], c=[0.0])  # flat line
        topology = toys.Topology(n_spatial=1, masses=[1.0], pes=pes)
        descriptor = peng.SnapshotDescriptor.construct(
            toys.Snapshot,
            {
                'n_atoms': 1,
                'n_spatial': 1
            }
        )
        engine = peng.NoEngine(descriptor)
        self.snap0 = toys.Snapshot(coordinates=np.array([[0.0]]),
                                   velocities=np.array([[1.0]]),
                                   engine=engine)
        self.snap1 = toys.Snapshot(coordinates=np.array([[0.1]]),
                                   velocities=np.array([[1.0]]),
                                   engine=engine)
        integrator = toys.LeapfrogVerletIntegrator(0.1)
        options = {
            'integ': integrator,
            'n_frames_max': 10000,
            'n_steps_per_frame': 5
        }
        self.engine = toys.Engine(options=options, topology=topology)
        self.cv = paths.FunctionCV("Id", lambda snap: snap.coordinates[0][0])
        self.left = paths.CVDefinedVolume(self.cv, float("-inf"), -1.0)
        self.right = paths.CVDefinedVolume(self.cv, 1.0, float("inf"))

        randomizer = paths.NoModification()
        self.filename = data_filename("shooting_analysis.nc")
        self.storage = paths.Storage(self.filename, mode="w")

        self.simulation = paths.CommittorSimulation(
            storage=self.storage,
            engine=self.engine,
            states=[self.left, self.right],
            randomizer=randomizer,
            initial_snapshots=[self.snap0, self.snap1]
        )
        self.simulation.output_stream = open(os.devnull, 'w')
        self.simulation.run(20)
        # set up the analysis object
        self.analyzer = ShootingPointAnalysis(self.storage.steps,
                                              [self.left, self.right])

    def teardown_method(self):
        import os
        paths.progress.HAS_TQDM = self.HAS_TQDM
        self.storage.close()
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        paths.EngineMover.default_engine = None  # set by Committor

    def test_overlapping_states(self):
        left2 = paths.CVDefinedVolume(self.cv, float("-inf"), -1.0)
        right2 = paths.CVDefinedVolume(self.cv, float("-inf"), -1.0)
        with pytest.raises(MoreStatesThanFramesError, match="overlap"):
            ShootingPointAnalysis(self.storage.steps, [self.left, left2,
                                                       self.right, right2])

    @pytest.mark.parametrize("accepted", [True, False])
    def test_no_endpoint_in_state(self, accepted):
        steps = [s for s in self.storage.steps]
        # break a step but also force it to be accepted/rejected
        broken_step = steps[-1]
        init_traj = broken_step.change.canonical.details.initial_trajectory
        broken_step.change.canonical.trials[0].trajectory = init_traj
        broken_step.change.canonical._accepted = accepted
        broken_step.mccycle = 123
        with pytest.raises(NoFramesInStateError, match="without endpoints"):
            ShootingPointAnalysis(steps, [self.left, self.right])

        # Make sure we don't raise if we don't want to error
        # and we warn more than once if multiple steps are wrong
        broken_step = steps[0]
        init_traj = broken_step.change.canonical.details.initial_trajectory
        broken_step.change.canonical.trials[0].trajectory = init_traj
        broken_step.change.canonical._accepted = accepted
        broken_step.mccycle = 321
        with pytest.warns(UserWarning) as warn:
            ShootingPointAnalysis(steps, [self.left, self.right],
                                  error_if_no_state=False)
            # Make sure we raise both warnings
            assert len(warn) == 2
            # Assert warnings come out in order of the step list
            assert "Step 321" in str(warn[0])
            assert "Step 123" in str(warn[1])

    def test_shooting_point_analysis(self):
        assert len(self.analyzer) == 2
        assert 0 < self.analyzer[self.snap0][self.left] < 20
        assert 0 < self.analyzer[self.snap0][self.right] < 20
        assert 0 < self.analyzer[self.snap1][self.left] < 20
        assert 0 < self.analyzer[self.snap1][self.right] < 20

    def test_from_individual_runs(self):
        runs = [(self.snap0, self.left),
                (self.snap0, self.left),
                (self.snap0, self.left),
                (self.snap0, self.right),
                (self.snap1, self.left),
                (self.snap1, self.right),
                (self.snap1, self.left),
                (self.snap1, self.right)]
        analyzer = ShootingPointAnalysis.from_individual_runs(runs)
        assert analyzer[self.snap0][self.left] == 3
        assert analyzer[self.snap0][self.right] == 1
        assert analyzer[self.snap1][self.left] == 2
        assert analyzer[self.snap1][self.right] == 2

    def test_non_shooting_steps(self):
        network = paths.TPSNetwork(self.left, self.right)
        init_traj = make_1d_traj([-1.1, 0.0, 1.1])
        ensemble = network.all_ensembles[0]
        mover = paths.PathReversalMover(ensemble)
        scheme = paths.LockedMoveScheme(mover, network)
        init_conds = scheme.initial_conditions_from_trajectories([init_traj])
        assert len(init_conds) == 1
        self.storage.close()
        self.storage = paths.Storage(self.filename, "w")
        assert init_conds[ensemble].trajectory == init_traj
        sim = paths.PathSampling(storage=self.storage,
                                 move_scheme=scheme,
                                 sample_set=init_conds)
        sim.output_stream = open(os.devnull, "w")
        sim.run(1)
        step0 = self.storage.steps[0]
        step1 = self.storage.steps[1]

        assert self.analyzer.step_key(step0) is None
        assert self.analyzer.step_key(step1) is None

        assert self.analyzer.analyze_single_step(step0) == []
        assert self.analyzer.analyze_single_step(step1) == []

    def test_committor(self):
        committor_A = self.analyzer.committor(self.left)
        committor_B = self.analyzer.committor(self.right)
        assert len(committor_A) == len(committor_B) == 2
        keys = [self.snap0, self.snap1]
        hashes0 = [self.analyzer.hash_function(k) for k in keys]
        for kA, kB in zip(list(committor_A.keys()), list(committor_B.keys())):
            hashA = self.analyzer.hash_function(kA)
            hashB = self.analyzer.hash_function(kB)
            assert hashA == hashB
            assert hashA in hashes0
            # hash is the same; snapshot is not
        for snap in committor_A:
            assert (committor_A[snap] ==
                    float(self.analyzer[snap][self.left]) / 20.0)
            assert pytest.approx(committor_A[snap] + committor_B[snap]) == 1.0
            assert (committor_B[snap] ==
                    float(self.analyzer[snap][self.right]) / 20.0)

        rehash = lambda snap: 2 * snap.xyz[0][0]
        committor_A_rehash = self.analyzer.committor(self.left, rehash)
        orig_values = sorted(committor_A.values())
        rehash_values = sorted(committor_A_rehash.values())
        assert_items_equal(orig_values, rehash_values)
        for snap in list(committor_A.keys()):
            assert rehash(snap) in list(committor_A_rehash.keys())

    def test_committor_histogram_1d(self):
        rehash = lambda snap: 2 * snap.xyz[0][0]
        input_bins = [-0.05, 0.05, 0.15, 0.25, 0.35, 0.45]
        hist, bins = self.analyzer.committor_histogram(rehash, self.left,
                                                       input_bins)
        assert len(hist) == 5
        for index in [1, 3, 4]:
            assert np.isnan(hist[index])
        for index in [0, 2]:
            assert hist[index] > 0
        assert_array_almost_equal(bins, input_bins)

    def test_committor_histogram_2d(self):
        rehash = lambda snap: (snap.xyz[0][0], 2 * snap.xyz[0][0])
        input_bins = [-0.05, 0.05, 0.15, 0.25, 0.35, 0.45]
        hist, b_x, b_y = self.analyzer.committor_histogram(rehash, self.left,
                                                           input_bins)
        assert hist.shape == (5, 5)
        for i in range(5):
            for j in range(5):
                if (i, j) in [(0, 0), (1, 2)]:
                    assert hist[(i, j)] > 0
                else:
                    assert np.isnan(hist[(i, j)])

        # this may change later to bins[0]==bins[1]==input_bins
        assert_array_almost_equal(input_bins, b_x)
        assert_array_almost_equal(input_bins, b_y)

    def test_committor_histogram_3d(self):
        # only 1D and 2D are supported
        rehash = lambda snap: (snap.xyz[0][0], 2 * snap.xyz[0][0], 0.0)
        input_bins = [-0.05, 0.05, 0.15, 0.25, 0.35, 0.45]
        with pytest.raises(RuntimeError, match="key dimension"):
            self.analyzer.committor_histogram(rehash, self.left, input_bins)

    def test_to_pandas(self):
        df1 = self.analyzer.to_pandas()
        df2 = self.analyzer.to_pandas(lambda x: x.xyz[0][0])
        assert df1.shape == (2, 2)
        assert_items_equal(df1.index, list(range(2)))
        assert_same_items(df2.index, [0.0, 0.1])
        assert_same_items(df1.columns, [self.left.name, self.right.name])
