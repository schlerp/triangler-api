/* tslint:disable */
/* eslint-disable */
/**
 * Triangler
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  ExperimentIn,
  ExperimentOut,
  JustId,
  Success,
} from '../models/index';
import {
    ExperimentInFromJSON,
    ExperimentInToJSON,
    ExperimentOutFromJSON,
    ExperimentOutToJSON,
    JustIdFromJSON,
    JustIdToJSON,
    SuccessFromJSON,
    SuccessToJSON,
} from '../models/index';

export interface ExperimentsApiCreateExperimentRequest {
    experimentIn: ExperimentIn;
}

export interface ExperimentsApiDeleteExperimentRequest {
    experimentId: number;
}

export interface ExperimentsApiGetExperimentByIdRequest {
    experimentId: number;
}

export interface ExperimentsApiUpdateExperimentRequest {
    experimentId: number;
    experimentIn: ExperimentIn;
}

/**
 *
 */
export class ExperimentsApi extends runtime.BaseAPI {

    /**
     * Creates a new experiment with the supplied payload, returns the experiment id.
     * Create Experiment
     */
    async experimentsApiCreateExperimentRaw(requestParameters: ExperimentsApiCreateExperimentRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<JustId>> {
        if (requestParameters.experimentIn === null || requestParameters.experimentIn === undefined) {
            throw new runtime.RequiredError('experimentIn','Required parameter requestParameters.experimentIn was null or undefined when calling experimentsApiCreateExperiment.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/v1/experiments`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: ExperimentInToJSON(requestParameters.experimentIn),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => JustIdFromJSON(jsonValue));
    }

    /**
     * Creates a new experiment with the supplied payload, returns the experiment id.
     * Create Experiment
     */
    async experimentsApiCreateExperiment(requestParameters: ExperimentsApiCreateExperimentRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<JustId> {
        const response = await this.experimentsApiCreateExperimentRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Deletes the experiment with a matching id.
     * Delete Experiment
     */
    async experimentsApiDeleteExperimentRaw(requestParameters: ExperimentsApiDeleteExperimentRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Success>> {
        if (requestParameters.experimentId === null || requestParameters.experimentId === undefined) {
            throw new runtime.RequiredError('experimentId','Required parameter requestParameters.experimentId was null or undefined when calling experimentsApiDeleteExperiment.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/v1/experiments/{experiment_id}`.replace(`{${"experiment_id"}}`, encodeURIComponent(String(requestParameters.experimentId))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => SuccessFromJSON(jsonValue));
    }

    /**
     * Deletes the experiment with a matching id.
     * Delete Experiment
     */
    async experimentsApiDeleteExperiment(requestParameters: ExperimentsApiDeleteExperimentRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Success> {
        const response = await this.experimentsApiDeleteExperimentRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Gets all experiments defined in this application.
     * Get All Experiments
     */
    async experimentsApiGetAllExperimentsRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<ExperimentOut>>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/v1/experiments`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(ExperimentOutFromJSON));
    }

    /**
     * Gets all experiments defined in this application.
     * Get All Experiments
     */
    async experimentsApiGetAllExperiments(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<ExperimentOut>> {
        const response = await this.experimentsApiGetAllExperimentsRaw(initOverrides);
        return await response.value();
    }

    /**
     * Get a specific experiemnt by its experiment ID.
     * Get Experiment By Id
     */
    async experimentsApiGetExperimentByIdRaw(requestParameters: ExperimentsApiGetExperimentByIdRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<ExperimentOut>> {
        if (requestParameters.experimentId === null || requestParameters.experimentId === undefined) {
            throw new runtime.RequiredError('experimentId','Required parameter requestParameters.experimentId was null or undefined when calling experimentsApiGetExperimentById.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/v1/experiments/{experiment_id}`.replace(`{${"experiment_id"}}`, encodeURIComponent(String(requestParameters.experimentId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => ExperimentOutFromJSON(jsonValue));
    }

    /**
     * Get a specific experiemnt by its experiment ID.
     * Get Experiment By Id
     */
    async experimentsApiGetExperimentById(requestParameters: ExperimentsApiGetExperimentByIdRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<ExperimentOut> {
        const response = await this.experimentsApiGetExperimentByIdRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Updates the experiment with `experiment id`, using supplied payload
     * Update Experiment
     */
    async experimentsApiUpdateExperimentRaw(requestParameters: ExperimentsApiUpdateExperimentRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Success>> {
        if (requestParameters.experimentId === null || requestParameters.experimentId === undefined) {
            throw new runtime.RequiredError('experimentId','Required parameter requestParameters.experimentId was null or undefined when calling experimentsApiUpdateExperiment.');
        }

        if (requestParameters.experimentIn === null || requestParameters.experimentIn === undefined) {
            throw new runtime.RequiredError('experimentIn','Required parameter requestParameters.experimentIn was null or undefined when calling experimentsApiUpdateExperiment.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/api/v1/experiments/{experiment_id}`.replace(`{${"experiment_id"}}`, encodeURIComponent(String(requestParameters.experimentId))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: ExperimentInToJSON(requestParameters.experimentIn),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => SuccessFromJSON(jsonValue));
    }

    /**
     * Updates the experiment with `experiment id`, using supplied payload
     * Update Experiment
     */
    async experimentsApiUpdateExperiment(requestParameters: ExperimentsApiUpdateExperimentRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Success> {
        const response = await this.experimentsApiUpdateExperimentRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
