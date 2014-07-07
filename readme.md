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
	
## Dependencies
- dateutil: `pip install python-dateutil`
