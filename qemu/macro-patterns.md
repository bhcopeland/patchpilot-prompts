# QEMU Macro Patterns

QEMU uses heavy preprocessor macros to synthesise types, struct fields, registration tables, and IR generators. A patch that changes a `VMSTATE_*` table or a `DEFINE_PROP_*` array often looks like it references undefined symbols — they are introduced by macro expansion, not by a normal C declaration.

When reviewing, **do not flag a symbol as "undefined" just because find_function / find_type returned no result**. Check whether it matches one of the families below; if it does, the symbol is real and synthesised by the macro.

QOM (`OBJECT_DECLARE_TYPE`, `OBJECT_DEFINE_TYPE`, `DEFINE_TYPES`, `OBJECT_CHECK`, etc.) is documented in QEMU's own qom-api.rst and will not be repeated here. The families below are the ones not auto-documented in headers.

## VMSTATE — migration field descriptors

In `include/migration/vmstate.h`. Used inside a `VMStateField fields[]` array within a `VMStateDescription`.

**Pattern**: `VMSTATE_<TYPE>(field_name, struct_name)` declares that a struct field participates in live-migration / vmstate save/load.

```c
static const VMStateDescription vmstate_foo = {
    .name = "foo",
    .version_id = 2,
    .fields = (VMStateField[]) {
        VMSTATE_UINT32(reg, FooState),
        VMSTATE_BOOL(enabled, FooState),
        VMSTATE_STRUCT(child, FooState, 0, vmstate_bar, BarState),
        VMSTATE_END_OF_LIST()
    }
};
```

Common variants:
- `VMSTATE_<INT>{8,16,32,64}` and `VMSTATE_BOOL`, `VMSTATE_BUFFER` — single fields
- `VMSTATE_ARRAY` and `VMSTATE_VARRAY_*` — fixed and variable-length arrays
- `VMSTATE_STRUCT[_ARRAY]` — embedded sub-struct
- `_V` suffix (e.g. `VMSTATE_UINT32_V`) — versioned, loaded only at version_id ≥ N
- `_TEST` suffix — conditional on a test predicate
- `VMSTATE_END_OF_LIST()` — sentinel terminator (every fields[] array needs one)

**Review notes**:
- Any change to vmstate ordering, types, or version is a migration-compatibility change. Check whether `version_id` / `minimum_version_id` were bumped.
- A field listed in vmstate must exist on the struct with that exact name and a compatible type.
- Removing a field without a versioned `_REMOVED` placeholder breaks live migration from older QEMUs.

## DEFINE_PROP_* — device properties

In `include/hw/qdev-properties.h`. Used in a `Property props[]` array attached via `device_class_set_props()`.

**Pattern**: `DEFINE_PROP_<TYPE>("name", DeviceState, field, default)` exposes a struct field as a settable device property (-device foo,name=value on the command line, or via QMP).

```c
static const Property foo_properties[] = {
    DEFINE_PROP_UINT32("size", FooState, size, 0x1000),
    DEFINE_PROP_BOOL("debug", FooState, debug, false),
    DEFINE_PROP_STRING("backend", FooState, backend),
    DEFINE_PROP_LINK("dma", FooState, dma_mr, TYPE_MEMORY_REGION, MemoryRegion *),
    DEFINE_PROP_END_OF_LIST()
};
```

There are ~40 type-specific variants (`DEFINE_PROP_DRIVE`, `DEFINE_PROP_NETDEV`, `DEFINE_PROP_PCIE_LINK_SPEED`, etc.) — they all expand to a `Property` struct entry.

**Review notes**:
- The named field must exist on the struct.
- `DEFINE_PROP_END_OF_LIST()` is required — every `Property[]` must terminate with it.
- Renaming or removing a property breaks command-line and QMP compatibility — usually wants a versioned alias kept around.

## memory_region_init_* — memory region constructors

In `include/exec/memory.h`. Despite looking like function calls, these are the canonical way to introduce a `MemoryRegion` into the address space hierarchy. Each member sets up a different kind of region:

| Macro | Backing | Typical use |
|---|---|---|
| `memory_region_init_ram` | malloc'd RAM | Plain RAM region |
| `memory_region_init_io` | `MemoryRegionOps` callbacks | MMIO with read/write handlers |
| `memory_region_init_rom` | const data | ROM (writes ignored or fault) |
| `memory_region_init_rom_device` | ROM read, callbacks for write | Flash-style devices |
| `memory_region_init_iommu` | IOMMU translation callbacks | DMA address translation |
| `memory_region_init_alias` | another MR | A window onto an existing region |

**Review notes**:
- Every region must be added to a parent address space with `memory_region_add_subregion(parent, offset, &child)` — or be the root.
- `MemoryRegionOps` for `_io` regions specifies read/write handlers and impl/valid byte widths; mismatched widths cause silent truncation.
- Aliases share lifetime with the underlying MR — outliving them is a use-after-free.

## qemu_irq + qdev_init_gpio_* — IRQ wires

In `include/hw/irq.h` and `include/hw/qdev-core.h`. `qemu_irq` is an opaque pointer for an interrupt or GPIO line.

```c
/* device side: declare incoming and outgoing lines */
qdev_init_gpio_in(dev, foo_set_irq, NUM_LINES);          /* incoming, named [0..NUM_LINES) */
qdev_init_gpio_out(dev, &state->irq_out, 1);             /* outgoing */
qdev_init_gpio_in_named(dev, foo_handler, "name", N);    /* incoming, named "name[0..N)" */

/* connecting from outside */
qdev_connect_gpio_out_named(src, "irq", 0, qdev_get_gpio_in(target, 0));

/* raising */
qemu_set_irq(state->irq_out[0], 1);
qemu_irq_raise(state->irq_out);    /* set high */
qemu_irq_lower(state->irq_out);    /* set low */
qemu_irq_pulse(state->irq_out);    /* high then low */
```

**Review notes**:
- A patch that adds new GPIO lines must also add them to vmstate if their state is migration-relevant.
- Naming must match between `qdev_init_gpio_*_named` and the connecting `qdev_connect_gpio_*_named` / `qdev_get_gpio_in_named`. Typos here are silent — the connection just doesn't happen.
- `qemu_irq` is a typedef for `qemu_irq *`; passing by value is correct, no `&`.

## sysbus_init_* — sysbus device wiring

In `include/hw/sysbus.h`. For SysBus devices (`TYPE_SYS_BUS_DEVICE`).

```c
sysbus_init_mmio(SYS_BUS_DEVICE(dev), &state->mmio_region);  /* MMIO window */
sysbus_init_irq(SYS_BUS_DEVICE(dev), &state->irq_out);       /* outgoing IRQ */
sysbus_mmio_map(sbd, 0, 0xfeed0000);                          /* place the Nth MMIO at addr */
sysbus_connect_irq(sbd, 0, target_irq);                       /* wire up the Nth IRQ */
```

The init calls register slots; the map/connect calls plug them into the platform.

## QLIST_*, QTAILQ_*, QSLIST_*, QSIMPLEQ_* — intrusive lists

In `include/qemu/queue.h`, lifted from BSD `queue.h`. Macros declare both the head/entry types and the manipulation operations.

```c
struct Foo {
    int x;
    QLIST_ENTRY(Foo) entry;          /* link field */
};

QLIST_HEAD(FooList, Foo);             /* declares struct FooList { struct Foo *lh_first; } */
struct FooList foos = QLIST_HEAD_INITIALIZER(foos);

QLIST_INSERT_HEAD(&foos, item, entry);
QLIST_REMOVE(item, entry);
QLIST_FOREACH(it, &foos, entry) { ... }
QLIST_FOREACH_SAFE(it, &foos, entry, next) { ... }   /* safe against removal */
```

The accessor names (`lh_first`, `le_next`) and `_ENTRY`/`_HEAD` typedefs are macro-synthesised. **Don't flag them as undefined** — they're real fields injected by `QLIST_ENTRY`/`QLIST_HEAD`.

The four prefixes:
- `QLIST_` — singly-linked, O(1) head insert/remove
- `QSLIST_` — singly-linked tail queue
- `QSIMPLEQ_` — simple queue with tail pointer
- `QTAILQ_` — doubly-linked tail queue (most common)

## TCG IR (`tcg_gen_*`)

In `include/tcg/tcg-op.h`. Used inside TCG translator code to emit the intermediate representation that becomes generated host code.

Naming convention: `tcg_gen_<op>_<size>` where size is `i32`, `i64`, or `tl` (target-long, the architecture's natural word).

```c
TCGv_i32 t = tcg_temp_new_i32();
tcg_gen_movi_i32(t, 42);
tcg_gen_add_i32(dst, src, t);
tcg_temp_free_i32(t);

TCGv addr = tcg_temp_new();        /* defaults to _tl */
tcg_gen_qemu_ld_tl(val, addr, mmu_idx, MO_LEUL);
```

Common families:
- `tcg_gen_mov[i]_<size>` — copy / load immediate
- `tcg_gen_{add,sub,and,or,xor,shl,shr,sar}[i]_<size>` — ALU
- `tcg_gen_brcond[i]_<size>` — conditional branch
- `tcg_gen_qemu_{ld,st}_<size>` — guest memory access (uses `MemOp` flags)
- `tcg_gen_movcond_<size>` — conditional move
- `tcg_gen_extract_<size>` / `_deposit_<size>` — bit-field operations

**Review notes**:
- `TCGv`, `TCGv_i32`, `TCGv_i64`, `TCGv_ptr` are typedefs to opaque structs — they appear "undefined" to a regex search but are real types.
- Every `tcg_temp_new_*` needs a matching `tcg_temp_free_*` in the same translation block — leaks are caught by an assertion at end-of-block but waste work.
- Mixing sizes (passing a `TCGv_i32` to an `_i64` op) is a compile error — but using `_tl` in a target-arch-specific file works because `tl` aliases the native size.

## What this means for review

When semcode's `find_function` or `find_type` returns "not found" for a symbol that looks like it belongs to one of these families:

- VMSTATE_* / DEFINE_PROP_* / QLIST_ENTRY_* members → real, synthesised by macro expansion. Don't flag.
- `qemu_irq`, `TCGv`, `TCGv_i32`, etc. → real typedefs in the headers above. Don't flag.
- `lh_first`, `tqe_next`, etc. (queue.h internals) → injected by QLIST_HEAD / QLIST_ENTRY. Don't flag.
- Functions like `qemu_set_irq`, `memory_region_add_subregion`, `tcg_gen_*`, `error_setg`, `qdev_*` → real public API. semcode may not have indexed them if they're declared via macros or in less common headers; do not assume "not found" means "doesn't exist".

When in doubt, `grep_functions` for the symbol with `path_pattern: "include/.*\\.h$"` to confirm it's defined somewhere in the headers before flagging it.
