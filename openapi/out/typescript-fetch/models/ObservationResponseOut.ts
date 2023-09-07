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

import { exists, mapValues } from '../runtime';
/**
 *
 * @export
 * @interface ObservationResponseOut
 */
export interface ObservationResponseOut {
    /**
     *
     * @type {number}
     * @memberof ObservationResponseOut
     */
    id?: number;
    /**
     *
     * @type {string}
     * @memberof ObservationResponseOut
     */
    chosenSample: string;
    /**
     *
     * @type {Date}
     * @memberof ObservationResponseOut
     */
    responseDate: Date;
    /**
     *
     * @type {number}
     * @memberof ObservationResponseOut
     */
    experiment: number;
    /**
     *
     * @type {number}
     * @memberof ObservationResponseOut
     */
    observation: number;
    /**
     *
     * @type {boolean}
     * @memberof ObservationResponseOut
     */
    isCorrect: boolean;
    /**
     *
     * @type {string}
     * @memberof ObservationResponseOut
     */
    experienceLevel: string;
}

/**
 * Check if a given object implements the ObservationResponseOut interface.
 */
export function instanceOfObservationResponseOut(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "chosenSample" in value;
    isInstance = isInstance && "responseDate" in value;
    isInstance = isInstance && "experiment" in value;
    isInstance = isInstance && "observation" in value;
    isInstance = isInstance && "isCorrect" in value;
    isInstance = isInstance && "experienceLevel" in value;

    return isInstance;
}

export function ObservationResponseOutFromJSON(json: any): ObservationResponseOut {
    return ObservationResponseOutFromJSONTyped(json, false);
}

export function ObservationResponseOutFromJSONTyped(json: any, ignoreDiscriminator: boolean): ObservationResponseOut {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {

        'id': !exists(json, 'id') ? undefined : json['id'],
        'chosenSample': json['chosen_sample'],
        'responseDate': (new Date(json['response_date'])),
        'experiment': json['experiment'],
        'observation': json['observation'],
        'isCorrect': json['is_correct'],
        'experienceLevel': json['experience_level'],
    };
}

export function ObservationResponseOutToJSON(value?: ObservationResponseOut | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {

        'id': value.id,
        'chosen_sample': value.chosenSample,
        'response_date': (value.responseDate.toISOString()),
        'experiment': value.experiment,
        'observation': value.observation,
        'is_correct': value.isCorrect,
        'experience_level': value.experienceLevel,
    };
}
