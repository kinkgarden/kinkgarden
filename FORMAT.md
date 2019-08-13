# List Format

To avoid storing lots of actual list data on the server, we bake the list into the URL
itself. To avoid making the URL incredibly long and difficult to work with, the list is
stored in the following binary format and Base64-encoded with `=` replaced with `!` for
query string non-weirdness purposes.

A List contains many Kinks. Since kinks are presented in columns, a Column ID is a two-bit
unsigned integer: 0 denotes the first column, 1 the second, 2 the third, and 3 the fourth.
There are two types of Kink: Standard and Custom. A Standard kink is stored in the
following sixteen-bit way:
```
00 0 00 000 00000000
├┘ │ ├┘ └──────────┴kink ID (matches up to database)
│  │ └Intensity flag (00=none specified, 01=light, 10=heavy, 11=extreme)
│  └Standard/Custom flag (must be 0 for standard)
└Column ID
```
There are 11 bits available for the kink ID, meaning that kink IDs up to 2047 can be
represented. This will likely be sufficient for all time.

A Custom kink is stored with the following 16-bit header, followed by a sequence of
UTF-8 text:
```
00 1 00 000 00000000
├┘ │ ├┘ └──────────┴text length (bytes)
│  │ └Intensity flag (00=none specified, 01=light, 10=heavy, 11=extreme)
│  └Standard/Custom flag (must be 1 for custom)
└Column ID
```
There are 11 bits available for the text length, meaning that up to 2047 bytes of UTF-8
can be stored in a Custom kink. The title and description of a Custom kink are separated
by a newline stored in that text field. 
