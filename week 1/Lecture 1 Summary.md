# Lecture 1: Summary

## Class Overview
- **Computer systems** for data science
- Very little math or algorithms
- Broad overview of computer systems and databases

## Performance Concepts and Rules of Thumb

### Throughput vs Latency
- Two orthogonal metrics to evaluate computer systems
- **Latency**: how long a single task takes
- **Throughput**: how many tasks are completed per unit of time

### Amdahl's Law
$$
Speedup(E) = \frac{ExTime_{old}}{ExTime_{new}} = \frac{1}{(1 - p) + \frac{p}{S}}
$$
- **p** = fraction of execution time that can be enhanced
- **S** = speedup of the enhanced portion
- **Speedup bounded by**: 1 / (fraction of time not enhanced)

### Time Scales in Computer Systems
Time scales can vary by millions:
- **CPUs and memory** operate in **nanoseconds**
- **Datacenter networks and SSDs** operate in **microseconds**
- **Sending stuff over the Internet** operates in **milliseconds**

## Intro to Datacenters
- Modern datacenter design: standard hardware, replicated in racks (cabinets), rows, deployed in football stadium-sized warehouses
