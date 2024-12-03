## Project Information

|                         |                           Details                            |
| :---------------------- | :----------------------------------------------------------: |
| Project Name            |                         Project ZII                          |
| Project Description     |       This is an example project for tutorial purposes       |
| Git Repository          | [snapp-express/ZII](https://git.zooket.ir/snapp-express/ZII) |
| Programming Language(s) |                           Markdown                           |

## Components

| Name     | Details                                            |
| :------- | ---------------------------------------------------|
| backend  | RESTful API server                                 |
| frontend | React app that integrates shows multiple swaggers  |

## Required Features

- [] Mounted Volume for Sqlite persistance
                    <ul>
                        <li>Estimated Data Size: `2G`</li>
                        <li>- [x] Persistent?</li>
                    </ul>

## Networking

#### Ingress[^1]

- [x] Public Domain
- [x] Internal Domain

| Component    | Type         | Domain                | Reason                                                       |
| ------------ | ------------ | --------------------- | ------------------------------------------------------------ |
| backend      | Internal     |                       | The Internal domain to provide api for gitlab runners        |
| backend      | Public       |                       | The public domain to provide api for React app               |
| frontend     | Internal     |                       | The internal domain is needed to publish a the React app     |

## Deployment

#### Resources

| Component    | Type    | Request     | Limit |
| ------------ | ------- | ----------- | ----- |
| backend      | Memory  | 500m        | 1g    |
| backend      | CPU     | 250m        | 1     |
| frontend     | Memory  | 1g          | 2g    |
| frontend     | CPU     | 1           | 2     |

#### Replicas

Requirements about how many instanecs of your application should be running simulatneously and if you need autoscaling (limits apply).

| Component | Replicas | Horizontal<br>Autoscaler |  Vertical<br>Autoscaler  |
| --------- | :------: | :----------------------: | :----------------------: |
| API       |    1     | <ul><li>- [ ] </ul></li> | <ul><li>- [x] </ul></li> |
| Panel     |    1     | <ul><li>- [ ] </ul></li> | <ul><li>- [x] </ul></li> |

# Release Checklist

In order for your project to be deployed into production environment there are some requirements that should be met.
This is an overall check list. You can see details of each item from the anchored markdown document.

| Item                                                                                                              | Passed                   |
| :---------------------------------------------------------------------------------------------------------------- | ------------------------ |
| [CI Pipelines](https://git.zooket.ir/snapp-express/ZII/-/blob/main/checklists/pipelines_checklist.md)  | <ul><li>- [ ] </li></ul> |
| [Database](https://git.zooket.ir/snapp-express/ZII/-/blob/main/checklists/database_checklist.md)       | <ul><li>- [ ] </li></ul> |
| [Logging](https://git.zooket.ir/snapp-express/ZII/-/blob/main/checklists/logging_checklist.md)         | <ul><li>- [ ] </li></ul> |
| [Monitoring](https://git.zooket.ir/snapp-express/ZII/-/blob/main/checklists/monitoring_checklist.md)   | <ul><li>- [ ] </li></ul> |
| [Performance](https://git.zooket.ir/snapp-express/ZII/-/blob/main/checklists/performance_checklist.md) | <ul><li>- [ ] </li></ul> |
| [Security](https://git.zooket.ir/snapp-express/ZII/-/blob/main/checklists/security_checklist.md)       | <ul><li>- [ ] </li></ul> |

<br><br><br>
***