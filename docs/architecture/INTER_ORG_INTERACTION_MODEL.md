# Inter-Organization Interaction Model

Execalc is designed to support secure collaboration between organizations without violating tenant isolation.

This model defines four structural components.

## Floor
The internal Execalc runtime operating within a single organization's tenant namespace.

## Fence
The tenant isolation boundary that prevents direct cross-organization access.

## Porch
A controlled intake layer that receives external signals before they enter the internal runtime.

Porches allow organizations to inspect, sanitize, and approve incoming strategic signals.

## Bridge
A protocol-based connection that allows one organization to send signals to another organization's porch.

Bridges never connect directly to internal runtime components.

## Interaction Example
Organization A sends a signal across a Bridge.
The signal arrives at Organization B's Porch.
The Porch evaluates and sanitizes the signal.
If approved, the signal may enter the internal runtime (Floor).

## Security Principle
No external signal may bypass the Porch layer.
