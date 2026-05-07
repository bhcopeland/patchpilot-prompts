# QEMU Technical Patterns

## Code style

- Four-space indentation, no tabs
- 80 character line width
- Traditional C comments only: /* */ not //
- Function opening brace on its own line
- if/else braces on same line as keyword
- All blocks must be braced, even single statements
- Variables: lower_case_with_underscores
- Types and structs: CamelCase
- Enums: CamelCase
- Function prefix: subsystem name for public functions
- Lock-held variants: _locked suffix

Checked by scripts/checkpatch.pl.

## Error handling (Error **errp)

This is the most common source of bugs in QEMU patches.

Rules:
- errp must be the last parameter
- Never examine *errp without ERRP_GUARD()
- Never touch *errp on success
- Set error or propagate on failure, never both
- Use error_setg() to create errors
- Use error_append_hint() for extra context

Wrong:
```c
if(*errp) { /* never do this without ERRP_GUARD() */ }
```

Right:
```c
ERRP_GUARD();
if(!some_function(errp)) {
  error_append_hint(errp, "context\n");
  return false;
}
```

## QOM (QEMU Object Model)

QEMU uses an object-oriented model in C. Key rules:

- parent_obj must be the first member of instance structs
- parent_class must be the first member of class structs
- Use OBJECT_DECLARE_TYPE() or OBJECT_DECLARE_SIMPLE_TYPE()
- Use DEFINE_PROP_* macros for device properties
- instance_init for lightweight setup (no errors)
- realize for allocation-heavy setup (takes Error **errp)
- unrealize must undo everything realize did

When reviewing QOM code:
- Check that parent is first member
- Check that realize/unrealize are balanced
- Check that properties use DEFINE_PROP macros
- Check type checker macros are correct

## Memory regions

Device models use memory regions for MMIO and PIO.

- memory_region_init_io() for MMIO with callbacks
- memory_region_init_alias() for mapping into other regions
- Pass OBJECT(dev) as owner
- MemoryRegionOps has .read and .write callbacks
- Handle endianness: DEVICE_NATIVE_ENDIAN, DEVICE_BIG_ENDIAN, etc.

When reviewing memory region code:
- Check that regions are unregistered before freeing
- Check that overlapping regions have correct priority
- Check endianness matches the device specification
- Check that .read/.write validate the access size

## Memory rules

- Use g_malloc(), g_new(), g_free() — never malloc/free
- Use g_try_new() for guest-controlled allocation sizes
- Use g_autofree and g_autoptr() for automatic cleanup
- Initialise g_autofree variables before any early return
- Use g_steal_pointer() when value must outlive the scope
- Prefer g_new(T, n) over g_malloc(sizeof(T) * n)

## Migration (vmstate)

QEMU saves and restores VM state for live migration and snapshots.

- VMStateDescription defines what fields are saved
- Fields must match between save and restore
- Adding fields needs version_id bump and minimum_version_id check
- Removing fields breaks backward compatibility
- VMSTATE_* macros must match the actual field type

When reviewing vmstate changes:
- Check version_id is bumped if fields change
- Check minimum_version_id is set correctly
- Check field types match between vmstate and struct
- Check that new fields have a default for old versions

## String handling

- pstrcpy() instead of strncpy() (guarantees NULL termination)
- pstrcat() for concatenation with bounds
- g_strdup() for dynamic strings
- qemu_isalnum() etc., not POSIX isalnum()

## Locking

- QEMU_LOCK_GUARD(&lock) for automatic unlock on exit
- WITH_RCU_READ_LOCK_GUARD() for RCU sections
- BQL (Big QEMU Lock) protects most device state
- vCPU threads need explicit locking for shared state

When reviewing locking:
- Check that BQL is held when accessing device state
- Check that QEMU_LOCK_GUARD is used instead of manual lock/unlock
- Check that vCPU thread access to shared state is protected

## Banned functions

QEMU bans certain functions. Use wrappers instead:

- malloc/calloc/realloc/free — use g_malloc/g_new/g_realloc/g_free
- strdup — use g_strdup
- strcpy/strncpy — use pstrcpy
- strcat — use pstrcat
- sprintf — use snprintf
- alloca — never use, not portable
- isalnum/isdigit/etc — use qemu_isalnum/qemu_isdigit/etc
