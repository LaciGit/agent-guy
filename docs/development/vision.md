
## Motivation
This is a *fun* project. It's not meant to be taken too seriously. Back in the days when I was a stundent at University of Applied Sciences `FH JOANNEUM` - in my master studies, I had some courses regarding `Agent-based modeling` [ABM]. I was never a big math or statistics guy; hence, the whole simulation area was not much interest to me. But when I started out with NetLogo and the basic principles of ABM, I got hooked.

## Inspiration
The project is highly inspired by established ABM tools and frameworks:

- [NetLogo](https://ccl.northwestern.edu/netlogo/)
- [Repast](https://repast.github.io/)
- [Mesa](https://mesa.readthedocs.io/en/stable/)
- [agentpy](https://agentpy.readthedocs.io/en/latest/)

Altough as a *classic* Data Engineer, I do not come across the use cases of ABM very often, I still like to play around with it. And that's what this project is about. It's a playground for me to try out new things and to learn new stuff. Furthermore, I want to incorporate some of the best practices I learned over the years in this project, in the context of Data Engineering.

## Simplicity
I would like to keep the usage of the package easy. Therefore I will try to build it so that the entry berrier is as low as possible. And for more advanced use cases, the goal should be to allow the user to extend the package with his own code. In other words, I really like how PREFECT has achieved this. The user can just drop the `@flow` decorator and use the `Flow` class to build his own flow. But an advanced user with the knowledge about the underlying concepts can build huge production ready workflows.

## Handling
I could imagine that the user starts out with a simple jupyter notebook or even a small UI (tkinter) to prepare the simulation. Once the simulation is ready to run, the user can just run the simulation in the background and analyze the results in the notebook or UI. Therefore, I would like to provide a simple API to start the simulation in the background and to get the results back to the notebook or UI.

## Technology Stack
As mentioned I would like to give the whole ABM a Data Engineering spin. Therefore, I will try to use the following technologies:

### Python
Python is my go-to language for Data Engineering. It's easy to learn, has a huge community and a lot of libraries. Furthermore, it's the language I am most familiar with. Since my Python experinece is limited to 3.9 I would like to try out some of the new features of Python 3.11.

### Distrubuted Computing
At a given point, an ABM is at the state that we would like to run 1000 of experiments and analyze the results. Therefore, we need to distribute the workload.

I am kind of familiar with PREFECT and DASK to perform distributed computing over a longer time period. Unfortunaly due to my responsibilites at work, I had to restirct the PREFECT version at a given point to provide stability. Regarding DASK, I really like the idea, user experinece and API since it is very close to numpy and pandas. However, I never had the chance to dive a little bit deeper into the topic. Therefore, I will try to use DASK and PREFECT in this project to get a better understanding of the technologies.
