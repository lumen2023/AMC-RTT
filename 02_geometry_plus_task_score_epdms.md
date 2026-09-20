# 02 Geometry Plus Task Score EPDMS

Status: `DIAGNOSTIC_ONLY`

Drive-JEPA used driving-specific outcome scores when constructing or auditing
consequence relations. In a generic toolkit, this layer becomes a
GeometryOutcomeRelation.

## Drive Version

Driving-specific relation evidence may combine:

```text
trajectory geometry
+ EPDMS / PDM-style consequence score
```

The exact Drive-JEPA score implementation is project-specific and must be read
from the current code before reuse. This file does not redefine EPDMS.

## Generic Version

For a new task:

```text
d_G(i,j) = geometry distance
J(y_i,c) = task outcome score or cost
```

A generic relation can use both:

```text
same_outcome(i,j) = close(J(y_i,c), J(y_j,c))
near_geometry(i,j) = d_G(i,j) <= epsilon
R_GO(i,j) = near_geometry(i,j) and same_outcome(i,j)
```

Potential replacements for driving EPDMS:

- success score;
- collision or violation cost;
- reward;
- goal achievement;
- contact quality;
- energy cost;
- safety margin.

## Claim Boundary

This layer is mainly for:

- oracle or reference relation construction;
- diagnostic upper bounds;
- transfer sanity checks.

Unless a task-specific experiment validates it as a training loss, do not claim
GeometryOutcomeRelation is the final deployable AMC objective.

