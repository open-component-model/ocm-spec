# Signature Algorithms

Signing a component descriptor requires a hash of the normalized component descriptor,
which will the be signed with the selected signing algorithm.

## RSA

*Algorith Name:* `RSASSA-PKCS1-V1_5`

After the digest for the normalised component descriptor is calculated, it can be signed using RSASSA-PKCS1-V1_5
as signature.algorithm. The corresponding signature is stored hex encoded in `signature.value` with a `mediaType` of
`application/vnd.ocm.signature.rsa`.
