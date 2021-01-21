# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

from resources import Session
from resources.db_classes import Transformer,Health_Index
#from imports.resources.Mixins import MixinsTables
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import datetime
import os

# path_r_square = 'src/imports/HI_calculation'
# import sys
# sys.path.append(path_r_square)
# import r_square

import tensorflow_addons as tfa


class WindowGenerator():
    def __init__(self, input_width, label_width, shift, train_df=None, val_df=None, test_df=None, infer_df=None, label_columns=None):
        
        # Store the data. Which comes in dictionaries of dataframes 
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

        # Work out the label column indices.
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
            self.column_indices = {name: i for i, name in enumerate(next(iter(train_df.values())).columns)}

        # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])

    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tf.stack([labels[:, :, self.column_indices[name]] for name in self.label_columns], axis=-1)

        # Slicing doesn't preserve static shape information, so set the shapes
        # manually. This way the `tf.data.Datasets` are easier to inspect.
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    def plot(self, model=None, plot_col='co', max_subplots=3):
        inputs, labels = self.example
        plt.figure(figsize=(12, 8))
        plot_col_index = self.column_indices[plot_col]
        max_n = min(max_subplots, len(inputs))
        for n in range(max_n):
            plt.subplot(3, 1, n+1)
            plt.ylabel(f'{plot_col} [normed]')
            plt.plot(self.input_indices, inputs[n, :, plot_col_index], label='Inputs', marker='.', zorder=-10)

            if self.label_columns:
                label_col_index = self.label_columns_indices.get(plot_col, None)
            else:
                label_col_index = plot_col_index

            if label_col_index is None:
                continue

            plt.scatter(self.label_indices, labels[n, :, label_col_index], edgecolors='k', label='Labels', c='#2ca02c', s=64)
            
            if model is not None:
                predictions = model(inputs)
                plt.scatter(self.label_indices, predictions[n, :, label_col_index], marker='X', edgecolors='k', label='Predictions', c='#ff7f0e', s=64)

            if n == 0:
                plt.legend()

        plt.xlabel('Time [h]')

    def make_dataset(self, data):

        for df in data.values():

            df = np.array(df, dtype=np.float32)
            ds = tf.keras.preprocessing.timeseries_dataset_from_array(
                data=df,
                targets=None,
                sequence_length=self.total_window_size,
                sequence_stride=1,
                shuffle=True,
                batch_size=32,)

            ds = ds.map(self.split_window)

            if 'final_ds' in locals():
                final_ds = final_ds.concatenate(ds)
            else:
                final_ds = ds

        return final_ds

    @property
    def train(self):
        return self.make_dataset(self.train_df)

    @property
    def val(self):
        return self.make_dataset(self.val_df)

    @property
    def test(self):
        return self.make_dataset(self.test_df)

    @property
    def example(self):
        """Get and cache an example batch of `inputs, labels` for plotting."""
        result = getattr(self, '_example', None)
        if result is None:
            # No example batch was found, so get one from the `.train` dataset
            result = next(iter(self.train))
            # And cache it for next time
            self._example = result
        return result


def collect_data(minyear=1990,maxyear=2020):

    session=Session()

    # -------------------------------------------------------
    # Lista dos nomes dos transformadores
    # -------------------------------------------------------

    trs = Transformer()
    trs_list = trs.get_batch(session)
    transfs=[transf.id_transformer for transf in trs_list]


    # -------------------------------------------------------
    # Criar um dicionário com os nomes das tables relevantes e 
    # dos respetivos campos de dados que serão transpostos para o df final
    # -------------------------------------------------------

    tables={}
    relationships=trs.__mapper__.relationships

    for relation in relationships:
        
        classs = relation.entity.class_
        name = classs.__name__

        if name == 'Weights' or name == 'Overall_Condition' or name == 'Maintenance_Scores': continue
        
        attrs = classs.__table__.columns.keys()
        attrs.remove(classs.__table__.primary_key.columns.keys()[0])
        attrs.remove('datestamp')
        attrs.remove('id_transformer')
        if name == 'Maintenance': attrs.remove('descript')
        if name == 'Health_Index': attrs.remove('id_algorithm'); attrs.remove('hi')
        if name == 'Load': attrs.remove('power_factor')

        tables[name] = attrs


    # -------------------------------------------------------
    # Criar o dicionário de dataframes com todos os dados da DB
    # -------------------------------------------------------

    # rawdf -> dicionário em que cada posição é um dataframe. Cada dataframe corresponde a um transf
    rawdf={}

    for trs_id in transfs:

        trs=Transformer(id_transformer=trs_id)

        # Inicializar dicionário pré-dataframe
        predf={}

        # inicializar vetores que vão constar no dicionário
        predf['year']=[]
        for table, attrs in tables.items():
            for attr in attrs:
                predf[attr]=[]
        for method_id in [1,2,3,4]:
            predf['hi'+str(method_id)]=[]

        # O verdadeiro ciclo    
        for year in range(minyear, maxyear+1):
            predf['year'].append(year)
            dict_queries = trs.get_by_time_interval(session, mindate=str(year)+'-01-01', maxdate=str(year)+'-12-31')
            
            for table, attrs in tables.items():
                query = dict_queries[table]
                
                if table=='Health_Index':
                    for method_id in [1,2,3,4]:
                        hi_subquery=query.filter(Health_Index.id_algorithm==method_id)
                        values = [getattr(value,'hi') for value in hi_subquery]
                        if values:
                            predf['hi'+str(method_id)].append(np.mean(values))
                        else:
                            predf['hi'+str(method_id)].append(np.nan)
                
                else:
                    for attr in attrs:
                        values = [getattr(measure,attr) for measure in query]
                        if values:
                            if attr=='impact_index':
                                predf[attr].append(np.sum(values))
                            else:
                                predf[attr].append(np.mean(values))
                        else:
                            predf[attr].append(np.nan)

        rawdf[trs_id] = pd.DataFrame(data=predf)

    session.close()

    # -------------------------------------------------------
    # Para o caso de ser preciso guardar os dataframes raw
    # -------------------------------------------------------

    # for transf in transfs:
    #     rawdf[transf].to_csv(path_or_buf='/home/bernardo/SEAI---Equipa-F/dados/dataframes/'+transf+'.csv')

    # -------------------------------------------------------
    # Cleaning and interpolating the dataframes
    # -------------------------------------------------------
    # A fazer: melhorar dropna para ter em conta todas as manutenções (no máximo, remover impact_index = 0)
    #          pensar como introduzir os dados das manutenções (soma em vez da média?)

    df = {}

    for transf in transfs:
        aux_rawdf = rawdf[transf].copy()

        # Separar medições dos HIs, em dataframes diferentes
        aux_df_hi=aux_rawdf.loc[: , "hi1":"hi4"]
        aux_df=aux_rawdf.drop(columns=['hi1','hi2','hi3','hi4'])

        # Interpolaçao linear para as medições / Sample and Hold para os HI
        aux_df = aux_df.interpolate(limit_area='inside')
        aux_df_hi = aux_df_hi.ffill()

        # Inverter HIs 1 e 3, para que o HI ótimo seja sempre o 100
        aux_df_hi[['hi1','hi3']] = 100 - aux_df_hi[['hi1','hi3']] 

        # Nova coluna com a média dos HIs por linha
        aux_df_hi['hi']=aux_df_hi.mean(axis=1)

        # Juntar tudo
        aux_df = aux_df.join(aux_df_hi['hi'])

        #Eliminar linhas vazias e extrapolar tipo "Sample&Hold", quando faltam valores nas pontas
        aux_df = aux_df.dropna(thresh=7).interpolate(limit_area='outside', limit_direction='both')
        
        #Eliminar algumas colunas
        #aux_df.drop(columns=['quantity','load_factor','breakdown_voltage'],inplace=True)

        df[transf] = aux_df.copy()
    
    return transfs, df


def training(IN_STEPS = 3, OUT_STEPS = 2, debug=False):

    transfs, df = collect_data()

    # -------------------------------------------------------
    # Separating year from data
    # -------------------------------------------------------

    year={}
    for trs in transfs:
        year[trs] = df[trs].pop('year')


    # -------------------------------------------------------
    # Train, Validation, Test split (0.8 / 0.2)
    # Split is done by transformers
    # -------------------------------------------------------

    column_indices = {name: i for i, name in enumerate(df[transfs[0]].columns)}
    num_features = df[transfs[0]].shape[1]

    nr = len(transfs)
    train_trs = transfs[:int(nr*0.8)]
    val_trs  = transfs[int(nr*0.8):]


    # -------------------------------------------------------
    # Getting mean and std of training data and normalizing all data
    # -------------------------------------------------------

    train_df = pd.DataFrame()

    for trs in train_trs:
        train_df = train_df.append(df[trs])

    train_mean = train_df.mean()
    train_std = train_df.std()

    for trs in transfs:
        df[trs] = (df[trs]- train_mean) / train_std

    # -------------------------------------------------------
    # Configuring the data windows
    # -------------------------------------------------------
    
    LABEL = ['hi']

    window = WindowGenerator(input_width  = IN_STEPS,
                            label_width   = OUT_STEPS,
                            shift         = OUT_STEPS,
                            train_df      = {trs : df[trs] for trs in train_trs},
                            val_df        = {trs : df[trs] for trs in val_trs},
                            #test_df       = {trs : df[trs] for trs in test_trs},
                            label_columns = LABEL)


    # -------------------------------------------------------
    # Checking the shape of input and output for each training batch
    # Each batch contains the information of one transformer
    # -------------------------------------------------------
    if debug:
        print('TRAINING BATCHES')
        print('Shape meaning: (windows,steps,features)\n')
        i=0
        for batch in window.train:
            inputs, targets = batch
            print('Batch', i+1, '- Transformer', train_trs[i], '-', len(df[train_trs[i]]), 'years') 
            print('Input  shape:',inputs.shape)
            print('Target shape:',targets.shape)
            print()
            i+=1

    # -------------------------------------------------------
    # Defining the model
    # -------------------------------------------------------

    n_neuronios=32
    paciencia=3
    velocidade_aprendizazem= 0.001 

    model = tf.keras.Sequential([
        # Shape [batch, time, features] => [batch, lstm_units]
        # Adding more `lstm_units` just overfits more quickly.
        tf.keras.layers.LSTM(n_neuronios, return_sequences=False),
        # Shape => [batch, out_steps*features]
        tf.keras.layers.Dense(4),
        tf.keras.layers.Dense(OUT_STEPS),
        # Shape => [batch, out_steps, features]
        tf.keras.layers.Reshape([OUT_STEPS, 1])
    ])

    # -------------------------------------------------------
    # Defining the training process, and training
    # -------------------------------------------------------

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=paciencia,
                                                    mode='min')

    model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError(),
                        tf.keras.metrics.RootMeanSquaredError(name='RMS_error', dtype=None),
                        tfa.metrics.r_square.RSquare(y_shape=(OUT_STEPS ,1))])

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    history = model.fit(window.train, epochs=100,
                        validation_data=window.val,
                        callbacks=[early_stopping, tensorboard_callback])

    if debug:
        print(model.summary())


    # -------------------------------------------------------
    # Final evaluation metrics
    # -------------------------------------------------------

    performance = model.evaluate(window.val, verbose=0)
    perf = pd.DataFrame(performance, index=model.metrics_names, columns =['Value'])

    model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError(),
                        tf.keras.metrics.RootMeanSquaredError(name='RMS_error', dtype=None)])

    model.save('transformers/ML/saved_model')

    return perf.to_dict()


# -------------------------------------------------------
# Plotting some examples
# -------------------------------------------------------
#window.plot(model, plot_col=LABEL[0])

def inference(debug=False):
    
    transfs, df = collect_data()

    model = tf.keras.models.load_model('transformers/ML/saved_model')


    IN_STEPS = model.input_shape[1]
    OUT_STEPS = model.output_shape[1]

    # -------------------------------------------------------
    # Separating year from data
    # -------------------------------------------------------

    year={}
    for trs in transfs:
        year[trs] = df[trs].pop('year')


    # -------------------------------------------------------
    # Train, Validation, Test split (0.8 / 0.2)
    # Split is done by transformers
    # -------------------------------------------------------

    column_indices = {name: i for i, name in enumerate(df[transfs[0]].columns)}
    num_features = df[transfs[0]].shape[1]


    # -------------------------------------------------------
    # Getting mean and std of training data and normalizing all data
    # -------------------------------------------------------

    total_df = pd.DataFrame()

    for trs in transfs:
        total_df = total_df.append(df[trs])

    train_mean = total_df.mean()
    train_std = total_df.std()

    for trs in transfs:
        df[trs] = (df[trs]- train_mean) / train_std

    
    # -------------------------------------------------------
    # Keeping only the last IN_STEPS rows
    # -------------------------------------------------------

    for trs in transfs:
        df[trs]=df[trs].tail(IN_STEPS)
        year[trs]=year[trs].tail(IN_STEPS)

    # # -------------------------------------------------------
    # # Configuring the data windows
    # # -------------------------------------------------------
    
    # LABEL = ['color']               #Alterar depois!!!!

    # window = WindowGenerator(input_width  = IN_STEPS,
    #                         label_width   = OUT_STEPS,
    #                         shift         = OUT_STEPS,
    #                         train_df      = df,
    #                         #val_df        = {trs : df[trs] for trs in val_trs},
    #                         #test_df       = df,
    #                         infer_df      = df,
    #                         label_columns = LABEL)


    # # -------------------------------------------------------
    # # Checking the shape of input and output for each training batch
    # # Each batch contains the information of one transformer
    # # -------------------------------------------------------
    # if debug:
    #     print('TRAINING BATCHES')
    #     print('Shape meaning: (windows,steps,features)\n')
    #     i=0
    #     for batch in window.train:
    #         inputs, targets = batch
    #         print('Batch', i+1, '- Transformer', train_trs[i], '-', len(df[train_trs[i]]), 'years') 
    #         print('Input  shape:',inputs.shape)
    #         print('Target shape:',targets.shape)
    #         print()
    #         i+=1

    pred={}
    for trs in transfs:
        input_np = np.expand_dims(df[trs].to_numpy(), axis=0)
        pred_np  = np.squeeze    (model.predict(input_np))
        
        pred[trs]={}
        for i in range(OUT_STEPS):
            yr = year[trs].tail(1).values[0] + 1 + i
            pred[trs][str(yr)]=float(pred_np[i])

    return pred




