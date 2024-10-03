import h5py
import numpy as np
import logging
import warnings
import os

PARENT_FIELD = dict(
    event_waveforms='events',
    event_sample_IDs='events',
    hyperparameter_latex_labels='hyperparameters',
    hyperparameter_descriptions='hyperparameters',
)

class PopulationResult:
    """
    class that allows multiple draws of event, injection, or fair population draws for each 
    population
    """
    def __init__(self, 
                fname=None,
                hyperparameters=None,
                hyperparameter_descriptions=None,
                hyperparameter_latex_labels=None,
                references=None,
                model_names=None,
                events=None,
                event_waveforms=None,
                event_sample_IDs=None,
                event_parameters=None):
        """
        Parameters
        ----------
        fname: str
            name of h5 file
        hyperparameters: list
            list of hyperparameters
        hyperparameter_descriptions: list
            list of hyperparameter descriptions
        hyperparameter_latex_labels: list
            list of latex labels for hyperparameters
        references: list
            list of references pointed to
        model_names: list
            list of population models used
        events: list
            list of events used
        event_waveforms: list or str
            list of waveforms in corresponding order to `events`
            or a single string denoting the waveform used for all events
        event_sample_IDs: list, int, or str
            list of IDs for PE sample versions in corresponding order to `events`
            or a single string/int denoting the version used for all events
        event_parameters: list
            list of event-level parameter names (e.g. m1, m2, chi_eff) in corresponding
            order to reweighted_event_samples, rewighted_injections and/or
            fair_population_draws
        """
        if not isinstance(fname, str):
            raise ValueError('filename must be given and must be a string')
        self.fname = fname
        if not os.path.exists(fname):
            logging.warning(f"Creating a new PopSummary file named {self.fname}")
            with h5py.File(fname, 'w') as f:
                f.create_group('posterior')
                f.create_group('prior')
                self.set_metadata('events', events)
                self.set_metadata('event_waveforms', event_waveforms)
                self.set_metadata('event_sample_IDs', event_sample_IDs)
                self.set_metadata('hyperparameters', hyperparameters)
                self.set_metadata('model_names', model_names)
                self.set_metadata('references', references)
                self.set_metadata('hyperparameter_latex_labels', hyperparameter_latex_labels)
                self.set_metadata('hyperparameter_descriptions', hyperparameter_descriptions)
                self.set_metadata('event_parameters', event_parameters)
        else:
            logging.warning(f"Opening existing PopSummary file named {self.fname}. To update anything in the file, use `set` functions")
        
    def get_metadata(self, field):
        """
        retrieve metadata from results file
        
        Parameters
        ----------
        field: str
            type of metadata to retrieve (e.g. 'events', 'model_names', etc.)
        """
        with h5py.File(self.fname, 'r') as f:
            if field in f.attrs.keys():
                return f.attrs[field]
            else:
                warnings.warn(f'metadata "{field}" does not exist')
                return None
    
    def set_metadata(self, field, metadata, overwrite=False):
        """
        saves metadata to results file
        
        Parameters
        ----------
        field: str
            type of metadata to save (e.g. 'events', 'model_names', etc.)
        metadata: str
            contents to save to field
        overwrite: bool
            whether to overwrite existing metadata
        """
        with h5py.File(self.fname, 'a') as f:
            if field in list(f.attrs.keys()):
                if overwrite:
                    del f.attrs[field]
                else:
                    raise Exception('metadata already exists, use the `overwrite` argument to overwrite it')
            if metadata is not None:
                if (field in PARENT_FIELD.keys()):
                    if PARENT_FIELD[field] not in f.attrs.keys():
                        raise Exception(f'`{PARENT_FIELD[field]}` must be assigned before `{field}`')
                    if isinstance(metadata, list) and (len(metadata) != len(f.attrs[PARENT_FIELD[field]])):
                        raise Exception(f'length of `{field}` ({len(metadata)}) must match length of '
                                        f'`{PARENT_FIELD[field]}` ({len(f.attrs[PARENT_FIELD[field]])})') 
                f.attrs[field] = metadata

    def get_hyperparameter_samples(self, hyper_sample_idx=None, hyperparameters=None, group='posterior'):
        """
        retrieve hyperparameter samples from results file
        
        Parameters
        ----------
        hyper_sample_idx: int or slice
            hyper samples to retrieve (None gives all hyper samples)
        hyperparameters: str or list of str
            name(s) of hyper-parameters to retrieve (None gives all parameters)
        group: str
            group to retrieve samples from ('posterior' or 'prior')

        Returns
        -------
        hyperparameter_samples: 2D array
            numpy array of data with shape (NumberOfHyperSamples,NumberOfPopulationDimensions)
        """
        with h5py.File(self.fname, 'r') as f:
            
            # select which hyperparameter draw number(s)
            mask_hyper_sample = self._mask_with_idx(selections=hyper_sample_idx)
                
            # select which hyper-parameter(s)
            mask_hyperparameter = self._mask_with_metadata(f, field='hyperparameters', selections=hyperparameters)
                
            return np.array(f[group]['hyperparameter_samples'])[mask_hyper_sample,:][:,mask_hyperparameter]

    def set_hyperparameter_samples(self, hyperparameter_samples, overwrite=False, group='posterior'):
        """
        save hyperparameter samples to results file
        
        Parameters
        ----------
        hyperparameter_samples: 2D array
            numpy array of data with shape (NumberOfHyperSamples,NumberOfPopulationDimensions)
        overwrite: bool
            whether to overwrite existing dataset
        group: str
            group to save samples to ('posterior' or 'prior')
        """
        # ensure hyperparameter_samples array is a numpy array
        hyperparameter_samples = np.asarray(hyperparameter_samples)

        with h5py.File(self.fname, 'a') as f:
            # do checks before writing data
            if 'hyperparameters' not in f.attrs.keys():
                raise Exception('metadata `hyperparameters` must be assigned before `hyperparameter_samples`')
            
            if hyperparameter_samples.ndim != 2:
                raise Exception(f'`hyperparameter_samples` should have 2-dimensions but has {hyperparameter_samples.ndim}')

            if hyperparameter_samples.shape[1] != len(f.attrs['hyperparameters']):
                raise Exception(f'axis-1 length of `hyperparameter_samples` ({hyperparameter_samples.shape[1]}) '
                                f'must match length of metadata `hyperparameters` ({len(f.attrs["hyperparameters"])})')
            if 'hyperparameter_samples' in list(f[group].keys()):
                if overwrite:
                    del f[group]['hyperparameter_samples']
                else:
                    raise Exception('dataset already exists, use the `overwrite` argument to overwrite it')

            # write data
            f[group].create_dataset('hyperparameter_samples', data=hyperparameter_samples)
        
    def get_reweighted_event_samples(self, events=None, draw_idx=None, hyper_sample_idx=None,
                                     use_hyperparameter_sample_idx_map=False, parameters=None, group="posterior"):
        """
        retrieve reweighted event samples from results file.

        Reweighted event samples are posterior samples for each GW event's properties
        such as mass_1, a_1, redshift, etc, but reweighted to the population
        described in the Popsummary file.
        
        Parameters
        ----------
        events: str or list of str
            names of events to retrieve samples from (None gives all events)
        draw_idx: int or slice
            draws to retrieve (None gives all draws)
        hyper_sample_idx: int or slice
            hyper samples to retrieve event samples for (None gives all hyper samples)        
        use_hyperparameter_sample_idx_map: bool, default False
            if `True` and the `hyperparameter_sample_idx_map` attribute is not `None`,
            the `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer
            to the indices of the array stored in the `reweighted_injections`
            data set along its third (`NumberOfHypersamples`) dimension. 
        parameters: str or list of str
            parameters to retrieve event samples for (None gives all parameters)
        group: str
            group to retrieve samples from ('posterior' or 'prior')

        Returns
        -------
        reweighted_event_samples: 4D array
            numpy array of data with shape
            (NumberOfEvents,NumberOfDraws,NumberOfHyperSamples,NumberOfEventDimensions)
        """
        with h5py.File(self.fname, 'r') as f:
            
            # select event(s)
            mask_event = self._mask_with_metadata(f, field='events', selections=events)
                
            # select which draw number(s)
            mask_draw = self._mask_with_idx(selections=draw_idx)

            # select which hyperparameter draw number(s)
            if use_hyperparameter_sample_idx_map:
                self._check_for_hyperparameter_sample_idx_map(f[group]['reweighted_event_samples'])
                mask_hyper_sample = self._mask_with_metadata(
                    f[group]['reweighted_event_samples'], 
                    'hyperparameter_sample_idx_map', 
                    hyper_sample_idx
                    )
                #mask_hyper_sample = self._map_hyperparameter_sample_idx(f[group]['reweighted_event_samples'],hyper_sample_idx)
            else:
                mask_hyper_sample = self._mask_with_idx(selections=hyper_sample_idx)

            # select which parameter(s)
            mask_parameter = self._mask_with_metadata(f, field='event_parameters', selections=parameters)

            return np.array(f[group]['reweighted_event_samples'])[mask_event,:,:,:][:,mask_draw,:,:][:,:,mask_hyper_sample,:][:,:,:,mask_parameter]
        
    def set_reweighted_event_samples(self, reweighted_event_samples, 
                                     hyperparameter_sample_idx_map=None,
                                     overwrite=False, group='posterior'):
        """
        save reweighted event samples to results file

        Reweighted event samples are posterior samples for each GW event's properties
        such as mass_1, a_1, redshift, etc, but reweighted to the population
        described in the Popsummary file.       

        Parameters
        ----------
        reweighted_event_samples: 4D array
            numpy array of data with shape
            (NumberOfEvents,NumberOfDraws,NumberOfHyperSamples,NumberOfEventDimensions)
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples.
            Should be used when reweighted_event_samples are calculated for only a subset
            of the hyperprior/posterior samples. `hypersample_idx_map` should hold the 
            indices for that subset from `hyperparameter_samples`. Default `None`.
        overwrite: bool
            whether to overwrite existing dataset
        group: str
            group to save samples to ('posterior' or 'prior')
        """
        # ensure we have numpy arrays
        reweighted_event_samples = np.asarray(reweighted_event_samples)

        with h5py.File(self.fname, 'a') as f:
            # do checks before writing
            if 'events' not in f.attrs.keys():
                raise Exception('metadata `events` must be assigned before `reweighted_event_samples`')
            if reweighted_event_samples.ndim!=4:
                raise Exception(f'`reweighted_event_samples` should have 4 dimensions but have {reweighted_event_samples.ndim}')
            if reweighted_event_samples.shape[0] != len(f.attrs['events']):
                raise Exception(f'axis-0 length of `reweighted_event_samples` ({reweighted_event_samples.shape[0]}) '
                                f'must match length of metadata `events` ({len(f.attrs["events"])})')
            if 'reweighted_event_samples' in list(f[group].keys()):
                if overwrite:
                    del f[group]['reweighted_event_samples']
                else:
                    raise Exception('dataset already exists, use the `overwrite` argument to overwrite it') 

            # write data    
            f[group].create_dataset('reweighted_event_samples', data=reweighted_event_samples)
            self._set_hyperparameter_sample_idx_map(f[group]['reweighted_event_samples'],hyperparameter_sample_idx_map)

    def get_reweighted_injections(self, events_idx=None, catalog_idx=None, hyper_sample_idx=None,
                                  use_hyperparameter_sample_idx_map=False,parameters=None, group="posterior"):
        """
        retrieve reweighted injections from results file.

        Reweighted injections are samples of detections found through mock
        injections into GW search pipelines (from some reference distribution), 
        reweighted to the population in this Popsummary file.  
        
        Parameters
        ----------
        events_idx: int or slice
            indices of simulated events in each "catalog" of simulated events from injections. 
            Each catalog has some number
            of reweighted injections, and these indices correspond to the indices
            of those reweighted injections that the user wants returned. (None gives all events)
        catalog_idx: int or slice
            catalogs to retrieve (None gives all catalogs)
        hyper_sample_idx: int or slice
            hyper samples to retrieve injections for (None gives all hyper samples)
        use_hyperparameter_sample_idx_map: bool, default False
            if `True` and the `hyperparameter_sample_idx_map` attribute is not `None`,
            the `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer
            to the indices of the array stored in the `reweighted_injections`
            data set along its third (`NumberOfHypersamples`) dimension. 
        parameters: str or list of str
            parameters to retrieve event samples for (None gives all parameters)
        group: str
            group to retrieve injections from ('posterior' or 'prior')

        Returns
        -------
        reweighted_injections: 4D array
            numpy array of data with shape
            (NumberOfEvents,NumberOfCatalogs,NumberOfHyperSamples,NumberOfInjectionDimensions)
        """
        with h5py.File(self.fname, 'r') as f:     
            # select event(s)
            mask_event = self._mask_with_idx(selections=events_idx)

            # select which draw number(s)
            mask_catalog = self._mask_with_idx(selections=catalog_idx)
                
            # select which hyper sample draw number(s)
            if use_hyperparameter_sample_idx_map:
                self._check_for_hyperparameter_sample_idx_map(f[group]['reweighted_injections'])
                mask_hyper_sample = self._mask_with_metadata(
                    f[group]['reweighted_injections'], 
                    'hyperparameter_sample_idx_map', 
                    hyper_sample_idx
                    )
                #mask_hyper_sample = self._map_hyperparameter_sample_idx(f[group]['reweighted_injections'],hyper_sample_idx)
            else:
                mask_hyper_sample = self._mask_with_idx(selections=hyper_sample_idx)
            
            # select which parameter(s)
            mask_parameter = self._mask_with_metadata(f, field='event_parameters', selections=parameters)
                
            return np.array(f[group]['reweighted_injections'])[mask_event,:,:,:][:,mask_catalog,:,:][:,:,mask_hyper_sample,:][:,:,:,mask_parameter]            
     

    def set_reweighted_injections(self, reweighted_injections, 
                                  hyperparameter_sample_idx_map=None,overwrite=False, group="posterior"):
        """
        save reweighted injections to results file
       
        Reweighted injections are samples of detections found through mock
        injections into GW search pipelines (from some reference distribution), 
        reweighted to the population in this Popsummary file. 

        Parameters
        ----------
        reweighted_injections: 4D array
            numpy array of data with shape
            (NumberOfInjections,NumberOfCatalogs,NumberOfHyperSamples,NumberOfInjectionDimensions)
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples.
            Should be used when reweighted_event_samples are calculated for only a subset
            of the hyperprior/posterior samples. `hypersample_idx_map` should hold the 
            indices for that subset from `hyperparameter_samples`. Default `None`.
        overwrite: bool
            whether to overwrite existing dataset
        group: str
            group to save injections to ('posterior' or 'prior')
        """
        # ensure we have a numpy array
        reweighted_injections = np.asarray(reweighted_injections)
        with h5py.File(self.fname, 'a') as f:
            # do checks before writing data
            if reweighted_injections.ndim!=4:
                raise Exception(f'`reweighted_injections` should have 4 dimensions but has {reweighted_injections.ndim}')
            if 'reweighted_injections' in list(f[group].keys()):
                if overwrite:
                    del f[group]['reweighted_injections']
                else:
                    raise Exception('dataset already exists, use the `overwrite` argument to overwrite it')

            # write data
            f[group].create_dataset('reweighted_injections', data=reweighted_injections)
            self._set_hyperparameter_sample_idx_map(f[group]['reweighted_injections'],hyperparameter_sample_idx_map)

            
    def get_fair_population_draws(self, draw_idx=None, hyper_sample_idx=None,
                                  use_hyperparameter_sample_idx_map=False, parameters=None, group="posterior"):
        """
        retrieve fair population draws from results file
        
        Parameters
        ----------
        draw_idx: int or slice
            draws to retrieve (None gives all draws)
        hyper_sample_idx: int or slice
            hyper samples to retrieve draws for (None gives all hyper samples)
        use_hyperparameter_sample_idx_map: bool, default False
            if `True` and the `hyperparameter_sample_idx_map` attribute is not `None`,
            the `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer
            to the indices of the array stored in the `reweighted_injections`
            data set along its third (`NumberOfHypersamples`) dimension. 
        parameters: str or list of str
            parameters to retrieve event samples for (None gives all parameters)
        group: str
            group to retrieve injections from ('posterior' or 'prior')

        Returns
        -------
        fair_population_draws: 3D array
            numpy array of data with shape
            (NumberOfDraws,NumberOfHyperSamples,NumberOfEventDimensions)
        """
        with h5py.File(self.fname, 'r') as f:     
                
            # select which draw number(s)
            mask_draw = self._mask_with_idx(selections=draw_idx)

            # select which hyper sample draw number(s)
            if use_hyperparameter_sample_idx_map:
                self._check_for_hyperparameter_sample_idx_map(f[group]['fair_population_draws'])
                mask_hyper_sample = self._mask_with_metadata(
                        f[group]['fair_population_draws'], 
                        'hyperparameter_sample_idx_map', 
                        hyper_sample_idx
                        )
                #mask_hyper_sample = self._map_hyperparameter_sample_idx(f[group]['fair_population_draws'],hyper_sample_idx)
            else:
                mask_hyper_sample = self._mask_with_idx(selections=hyper_sample_idx)

            # select which parameter(s)
            mask_parameter = self._mask_with_metadata(f, field='event_parameters', selections=parameters)
                
            return np.array(f[group]['fair_population_draws'])[mask_draw,:,:][:,mask_hyper_sample,:][:,:,mask_parameter] 

        
    def set_fair_population_draws(self, fair_population_draws, 
                                  hyperparameter_sample_idx_map=None,overwrite=False, group="posterior"):
        """
        save fair population draws to results file
        
        Parameters
        ----------
        fair_population_draws: 3D array
            numpy array of data with shape
            (NumberOfDraws,NumberOfHyperSamples,NumberOfEventDimensions)
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples.
            Should be used when reweighted_event_samples are calculated for only a subset
            of the hyperprior/posterior samples. `hypersample_idx_map` should hold the 
            indices for that subset from `hyperparameter_samples`. Default `None`.
        overwrite: bool
            whether to overwrite existing dataset
        group: str
            group to save draws to ('posterior' or 'prior')
        """
        # ensure a numpy array
        fair_population_draws = np.asarray(fair_population_draws)
        
        with h5py.File(self.fname, 'a') as f:
            # do checks on inputs
            if fair_population_draws.ndim!=3:
                raise Exception(f'`fair_population_draws` should have 3 dimensions but has {fair_population_draws.ndim}')
            if 'fair_population_draws' in list(f[group].keys()):
                if overwrite:
                    del f[group]['fair_population_draws']
                else:
                    raise Exception('dataset already exists, use the `overwrite` argument to overwrite it') 
            
            # write data
            f[group].create_dataset('fair_population_draws', data=fair_population_draws)
            self._set_hyperparameter_sample_idx_map(f[group]['fair_population_draws'],hyperparameter_sample_idx_map)
            
    def get_rates_on_grids(self, grid_key, hyper_sample_idx=None,
                           use_hyperparameter_sample_idx_map=False,
                           return_params=False, return_attributes=None, group="posterior"):
        """
        retrieve rates on grids from results file (positions, rates,
                                                   params [optional], attributes [optional])
        
        Parameters
        ----------
        grid_key: str
            key for rates dataset (e.g. 'primary_mass')
        hyper_sample_idx: int or slice
            hyper samples to retrieve rates for (None gives all hyper samples)
        use_hyperparameter_sample_idx_map: bool, default False
            if `True` and the `hyperparameter_sample_idx_map` attribute is not `None`,
            the `hyper_sample_idx` array specified will refer to indices of the
            `hyperparameter_samples`. If `False`, `hyper_sample_idx` will refer
            to the indices of the array stored in the
            data set along its (`NumberOfHypersamples`) dimension. 
        return_params: bool
            whether to return parameter labels for grid
        return_attributes: bool, str or list
            optional additional attributes to return as dict
            if True, returns all attributes
            (returns after params if return_params=True)
        group: str
            group to retrieve injections from ('posterior' or 'prior')
        
        Returns
        -------
        positions: 2D array
            numpy array of grid positions at which rates are calculated with shape
            `(NumberOfParameters, NumberOfGridPoints)`
        rates: 2D array
            numpy array of rates calculated on grid with shape
            `(NumberOfHypersamples, NumberOfGridPoints)`. 
            This represents either the rate or pdf at a 
            given grid point for a given hypersample.
        grid_params: str or list
            list of parameter names for which rates are calculated, returned if `return_params=True`      
        attributes: string or list
            list of optional additional attributes, returned if `return_attributes` specified
        """
        with h5py.File(self.fname, 'r') as f:
            
            # select which hyper sample draw number(s)
            if hyper_sample_idx is None:
                mask_hyper_sample = slice(None)
            else:
                if use_hyperparameter_sample_idx_map:
                    self._check_for_hyperparameter_sample_idx_map(f[group]['rates_on_grids'][grid_key])
                    mask_hyper_sample = self._mask_with_metadata(
                        f[group]['rates_on_grids'][grid_key], 
                        'hyperparameter_sample_idx_map', 
                        hyper_sample_idx
                        )
                    #mask_hyper_sample = self._map_hyperparameter_sample_idx(f[group]['fair_population_draws'],hyper_sample_idx)
                else:
                    mask_hyper_sample = self._mask_with_idx(selections=hyper_sample_idx)

            ret = (np.array(f[group]['rates_on_grids'][grid_key]['positions']),
                   np.array(f[group]['rates_on_grids'][grid_key]['rates'])[mask_hyper_sample, ...],)
            
            if return_params:
                ret += (f[group]['rates_on_grids'][grid_key].attrs['parameters'],)
            if return_attributes is not None:
                ret_attrs = dict()
                if return_attributes == True:
                    for attribute in f[group]['rates_on_grids'][grid_key].attrs:
                        ret_attrs[attribute] = f[group]['rates_on_grids'][grid_key].attrs[attribute]
                elif isinstance(return_attributes, list):
                    for attribute in return_attributes:
                        ret_attrs[attribute] = f[group]['rates_on_grids'][grid_key].attrs[attribute]
                else:
                    ret_attrs[return_attributes] = f[group]['rates_on_grids'][grid_key].attrs[return_attributes]
                ret += (ret_attrs,)
            return ret
        
    def set_rates_on_grids(self, grid_key, grid_params, positions, rates,
                           hyperparameter_sample_idx_map=None,
                           attribute_keys=None, attributes=None,
                           overwrite=False, group="posterior"):
        """
        save rates on grids to results file
        
        Parameters
        ----------
        grid_key: str
            key for rates dataset (e.g. 'primary_mass')
        grid_params: str or list
            list of parameter names for which rates are calculated
        positions: 2D array
            numpy array of grid positions at which rates are calculated with shape
            `(NumberOfParameters, NumberOfGridPoints)`. 
            The grid positions need not be a rectangular grid. 
            Each `NumberOfParameters`-dimensional point at which the 
            rate/PDF is evaluated is written out. There are 
            `NumberOfGridPoints` points at which the rate/PDF 
            is evaluated.
        rates: 2D array
            numpy array of rates calculated on grid with shape
            `(NumberOfHypersamples, NumberOfGridPoints)`. 
            This represents either the rate or pdf at a 
            given grid point for a given hypersample.
        hyperparameter_sample_idx_map: array, optional
            Array of indices that map to the corresponding hyperprior/posterior samples.
            Should be used when data set corresponds to a subset
            of the hyperprior/posterior samples. `hyperparameter_sample_idx_map` should hold the 
            indices for that subset from `hyperparameter_samples`. Default `None`.
        attribute_keys: string or list
            list of keys for optional additional attributes
            (must match length of attributes)
        attributes: string or list
            list of optional additional attributes
            (must match length of attribute_keys)
        overwrite: bool
            whether to overwrite existing dataset
        group: str
            group to save draws to ('posterior' or 'prior')
        """

        # ensure numpy arrays
        positions = np.atleast_2d(positions)
        rates = np.asarray(rates)

        # do checks on inputs
        if positions.ndim!=2:
            raise Exception(f'`positions` should have 2 dimensions but has {positions.ndim}')
        if rates.ndim!=2:
            raise Exception(f'`rates` should have 2 dimensions but has {rates.ndim}')  
      
        # check grid params and positions have commensurable shapes
        if isinstance(grid_params,str):
            grid_params = [grid_params]
        if len(grid_params)!=positions.shape[0]:
            raise Exception('`grid_params` should have same length as 0th axis of `positions`')
        
        with h5py.File(self.fname, 'a') as f:
            if 'rates_on_grids' not in list(f[group].keys()):
                f[group].create_group('rates_on_grids')
            if grid_key in list(f[group]['rates_on_grids'].keys()):
                if overwrite:
                    del f[group]['rates_on_grids'][grid_key]
                else:
                    raise Exception('dataset already exists, use the `overwrite` argument to overwrite it')
            f[group]['rates_on_grids'].create_group(grid_key)
            f[group]['rates_on_grids'][grid_key].attrs['parameters'] = grid_params
            f[group]['rates_on_grids'][grid_key].create_dataset('positions', data=positions)
            f[group]['rates_on_grids'][grid_key].create_dataset('rates', data=rates)
            self._set_hyperparameter_sample_idx_map(f[group]['rates_on_grids'][grid_key],hyperparameter_sample_idx_map)

            if attributes is not None:
                if type(attributes) == list:
                    for attr_idx in range(len(attributes)):
                        f[group]['rates_on_grids'][grid_key].attrs[attribute_keys[attr_idx]] = attributes[attr_idx]
                else:
                    f[group]['rates_on_grids'][grid_key].attrs[attribute_keys] = attributes
    
    def _check_for_hyperparameter_sample_idx_map(self,dataset):
        """check that a `hyperparameter_sample_idx_map`
        has been defined
        """
        if isinstance(dataset.attrs['hyperparameter_sample_idx_map'],str):
            raise Exception('a `hyperparameter_sample_idx_map` has not been defined')
            
    def _set_hyperparameter_sample_idx_map(self,dataset, hyperparameter_sample_idx_map):
        """
        dataset: h5 data set
        hyperparameter_sample_idx_map: array
            array of indices specifying which subset of elements in `hyperparameter_samples`
            correspond to the elements in a dataset of interest
        """
        if hyperparameter_sample_idx_map is None: # h5 attr cannot save None, must save 'None' string
            dataset.attrs['hyperparameter_sample_idx_map'] = 'None'
        else:
            dataset.attrs['hyperparameter_sample_idx_map'] = hyperparameter_sample_idx_map

                
    def _mask_with_idx(self, selections):
        if selections is None:
            mask = slice(None)
        else:
            if (not isinstance(selections, (list,np.ndarray))) and (not isinstance(selections, slice)):
                mask = [selections]
            else:
                mask = selections
        return mask
    
    def _mask_with_metadata(self, f, field, selections):
        if selections is None:
            mask = slice(None)
        else:
            if isinstance(selections, (list,np.ndarray)):
                mask = [np.flatnonzero(f.attrs[field] == selection)[0] for selection in selections]
            else:
                mask = np.flatnonzero(f.attrs[field] == selections)
        return mask
