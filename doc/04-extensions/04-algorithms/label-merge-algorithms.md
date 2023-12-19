# Label Merge Algorithms

If no specific algorithm is configured for a label, the algorithm used is `default`.
 
There is a set of globally defined standard algorithms:
 
- `default`  just decide for one side or reject the transfer.
 
  It used the following configuration fields:

  - `overwrite` *string*: specify the behaviour in case of a conflict. The following configuration values are possible:

    - `none`: reject changes

    - `local`: keep the local value found in the target 

    - `inbound` overwrite the local value with the transferred values. THis is the default for this merge algorithm

- `simpleListMerge`: just merge the list.

   The resulting value will contain all the entries of

   the inbound and the local version.
 
- `simpleMapMerge`: just merge the elements of a map.

  The resulting value will contain all the entries of

  the inbound and the local version. In case of a 

  conflict the entry is merged according the selected overwrite mode ( default `none`)
 
  The following configuration values are possible:

  - `overwrite` *string*: conflict resolution hint (see `default`).

  - `entries` [*merge spec*](../../specification/formats/formats.md#label-specifications): merge specification to be used for conflicting entries.

  If no overwrite mode is selected AND the `entries` field is given, conflicting entries will be merged with the specified merge specification  Otherwise, the default resolution is `none`-
 
- `simplemMapListNerge` merge maps used as list entries.
 
  If a list contains map entries which feature an identity, list entries with the same identity can be merged.

  This algorithm uses a key field in the maps to detect their identity.
 
  The following configuration values are possible:

  - `overwrite` *string*: conflict resolution hint (see `default`).

  - `entries` [*merge spec*](../../specification/formats/formats.md#label-specifications): merge specification to be used for conflicting entries.
 
  If no overwrite mode is selected AND the `entries` field is given, conflicting entries will be merged with the specified merge specification. Otherwise, the default resolution is `none`-
 
All algorithms supporting cascading of merge algorithms for their element (in the meaning defined by the algorithm) SHOULD offer such a merge specification field complying to the standard fields of a merge specification. It is a good practice to use an unset `overwrite` conflict resolution field to enable the cascading and support the other standard options, also.
 
Standard algorithms always use flat names. All non-standard algorithms must use a hierarchical name prefixed at least with a DNS-like domain owned by the provider of the algorithm.
