## Features
### To Add
- define search parameters
	- modified by [user]
	- modified between [date range]
	- chose Box or local modified time 
- multi-step process
	- generate matched search results
	- take search results and execute revert
		- allows users opportunity to edit files to modify
- output logging

## Notes
### Authentication
- Use `export BOX_ACCESS_TOKEN=MYTOKEN` in terminal to set environment variable

### Identifying files
- "content_modified_at" may be more useful than "modified_at" for identifying content that has been locally affected by cryptolocker.
  - see: [Content Times](http://developers.box.com/content-times/)
- Box uses ISO 8601 format timestamps
	- in Python, use `datetime.isoformat([sep])`

## Cases to test
- positive: file modified after target date
- negative: file modified before target date
- negative: file create after target date (new file, not corrupted, no version history)
- ?: multiple versions after target date
- negative: file has already been reverted (related to above)
	
## Dependencies
- dateutil: `pip install python-dateutil`
