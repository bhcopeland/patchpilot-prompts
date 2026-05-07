# QEMU False Positive Guide

Things that look like bugs but are not in the QEMU codebase.

## error_propagate is not a bug

Old code uses error_propagate() with a local Error *local_err.
New code should use ERRP_GUARD() instead. The old pattern is not
a bug, just outdated style. Do not flag it unless the patch
introduces new error_propagate() usage.

## g_malloc exits on failure

g_malloc() and g_new() abort on allocation failure by default.
Do not report "missing NULL check after g_malloc". The program
exits before returning NULL.

Only g_try_malloc() and g_try_new() can return NULL and need
a NULL check.

## g_autofree variables

```c
g_autofree char *str = NULL;
```

This is not a leak. g_autofree frees the variable when it goes
out of scope. The = NULL initialisation is required so early
returns do not free garbage.

## vmstate looks like duplication

VMStateDescription fields look like they duplicate the struct
definition. This is intentional and necessary for migration.
Do not flag it as code duplication.

## BQL is implicit in some contexts

Device model callbacks (.realize, .reset, property setters) run
under the BQL by default. Do not report missing locking in these
contexts unless the code explicitly drops the BQL.

## Long device model names

Device model type names can be long:
```c
TYPE_VIRTIO_IOMMU_PCI
```

This is normal. Do not flag long identifiers in device models.

## Bitfields in existing code

QEMU discourages new bitfields but has them in existing code.
Do not flag existing bitfields unless the patch changes them.

## Mixed old and new error patterns

Some files mix error_propagate() and ERRP_GUARD(). This is
migration in progress, not a bug. Only flag if the patch adds
new error_propagate() where ERRP_GUARD() should be used.

## Cast to/from void pointers

QEMU often casts between typed and void pointers for opaque
callback data. This is normal C practice, not a type safety
issue.

## OBJECT_CHECK and OBJECT_CLASS_CHECK

Old code uses these macros directly. New code uses the generated
checkers from OBJECT_DECLARE_TYPE(). Both are correct. Do not
flag the old style unless the patch introduces it.
